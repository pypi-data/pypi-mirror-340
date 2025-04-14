import pandas as pd
import numpy as np
from typing import Tuple, Dict, Union, Optional, List
from sklearn.ensemble import RandomForestClassifier  # Import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from concurrent.futures import ThreadPoolExecutor, as_completed
from sklearn.isotonic import IsotonicRegression
from scipy import stats
# =========================
# Enhanced Monotonic Binning
# =========================

def mono_bin(Y: Union[pd.Series, np.ndarray],
             X: Union[pd.Series, np.ndarray],
             n: int = 10,
             min_bin_size: float = 0.05,
             alpha: float = 0.5,
             force_trend: Optional[str] = None,
             var_name: str = "VAR") -> Tuple[pd.DataFrame, Dict]:

    Y = pd.Series(Y).reset_index(drop=True)
    X = pd.Series(X).astype(float).reset_index(drop=True)
    valid_mask = X.notna()
    X_valid, Y_valid = X[valid_mask], Y[valid_mask]

    if len(X_valid) == 0 or X_valid.nunique() <= 1:
        return pd.DataFrame(), {np.nan: 0.0}

    try:
        bins = pd.qcut(X_valid, q=min(n, len(X_valid)), duplicates='drop')
    except ValueError:
        try:
            bins = pd.qcut(X_valid, q=min(5, len(X_valid)), duplicates='drop')
        except ValueError:
            bins = pd.cut(X_valid, bins=min(5, len(X_valid)))

    df_binned = pd.DataFrame({'X': X_valid, 'Y': Y_valid, 'BIN': bins})
    bin_stats = (
        df_binned.groupby('BIN', observed=True)
        .agg(
            MIN_VALUE=('X', 'min'),
            MAX_VALUE=('X', 'max'),
            COUNT=('Y', 'count'),
            EVENT=('Y', 'sum')
        )
        .assign(NONEVENT=lambda x: x['COUNT'] - x['EVENT'])
        .sort_values('MIN_VALUE')
    )

    total_events = max(Y_valid.sum(), 1e-10)
    total_nonevents = max(len(Y_valid) - total_events, 1e-10)

    bin_stats['EVENT_RATE'] = (bin_stats['EVENT'] + alpha) / (total_events + alpha * len(bin_stats))
    bin_stats['NON_EVENT_RATE'] = (bin_stats['NONEVENT'] + alpha) / (total_nonevents + alpha * len(bin_stats))

    if force_trend is not None:
        iso = IsotonicRegression(increasing=(force_trend == 'i'), out_of_bounds='clip')
        bin_stats['EVENT_RATE'] = iso.fit_transform(
            bin_stats.index.categories.mid, bin_stats['EVENT_RATE']
        )

    ratio = np.divide(bin_stats['EVENT_RATE'], bin_stats['NON_EVENT_RATE'])
    bin_stats['WOE'] = np.log(np.clip(ratio, 1e-10, 1e10)).replace([np.inf, -np.inf, np.nan], 0)
    bin_stats['IV'] = (bin_stats['EVENT_RATE'] - bin_stats['NON_EVENT_RATE']) * bin_stats['WOE']

    woe_map = {}
    for _, row in bin_stats.iterrows():
        woe_map[(row['MIN_VALUE'], row['MAX_VALUE'])] = float(row['WOE'])

    if len(bin_stats) > 0:
        woe_map[(-np.inf, bin_stats['MIN_VALUE'].min())] = float(bin_stats['WOE'].iloc[0])
        woe_map[(bin_stats['MAX_VALUE'].max(), np.inf)] = float(bin_stats['WOE'].iloc[-1])

    if not valid_mask.all():
        missing_events = Y[~valid_mask].sum()
        missing_nonevents = (~valid_mask).sum() - missing_events
        missing_ratio = (missing_events + alpha) / (missing_nonevents + alpha)
        woe_map[np.nan] = float(np.log(max(min(missing_ratio, 1e10), 1e-10)))

    bin_stats.insert(0, "VAR_NAME", var_name)
    return bin_stats.replace([np.inf, -np.inf], np.nan), woe_map

def char_bin(Y: Union[pd.Series, np.ndarray],
             X: Union[pd.Series, np.ndarray],
             var_name: str = "VAR",
             alpha: float = 0.5) -> Tuple[pd.DataFrame, Dict]:

    X = pd.Series(X).fillna('MISSING').replace(['nan', 'None', ''], 'MISSING')
    Y = pd.Series(Y)

    grouped = pd.DataFrame({'X': X, 'Y': Y}).groupby('X', observed=True)
    bin_stats = pd.DataFrame({
        'VAR_NAME': var_name,
        'CATEGORY': list(grouped.groups.keys()),
        'COUNT': grouped.count().Y,
        'EVENT': grouped.sum().Y
    })
    bin_stats['NONEVENT'] = bin_stats['COUNT'] - bin_stats['EVENT']

    total_events = max(Y.sum(), 1e-10)
    total_nonevents = max(len(Y) - Y.sum(), 1e-10)

    bin_stats['EVENT_RATE'] = (bin_stats['EVENT'] + alpha) / (total_events + alpha * len(bin_stats))
    bin_stats['NON_EVENT_RATE'] = (bin_stats['NONEVENT'] + alpha) / (total_nonevents + alpha * len(bin_stats))

    ratio = bin_stats['EVENT_RATE'] / bin_stats['NON_EVENT_RATE']
    bin_stats['WOE'] = np.where((ratio > 0), np.log(np.clip(ratio, 1e-10, 1e10)), 0)
    bin_stats['IV'] = (bin_stats['EVENT_RATE'] - bin_stats['NON_EVENT_RATE']) * bin_stats['WOE']

    woe_map = {np.nan if k == 'MISSING' else k: v for k, v in zip(bin_stats['CATEGORY'], bin_stats['WOE'])}
    return bin_stats.replace([np.inf, -np.inf], np.nan), woe_map

# =========================
# Parallel IV/WOE Worker
# =========================

def _iv_worker(args):
    df, target, feature, alpha = args
    if pd.api.types.is_numeric_dtype(df[feature]) and df[feature].nunique() > 2:
        bin_stats, woe_map = mono_bin(df[target], df[feature], var_name=feature, alpha=alpha)
    else:
        bin_stats, woe_map = char_bin(df[target], df[feature], var_name=feature, alpha=alpha)
    return feature, bin_stats, woe_map


# =========================
# Main IV Function with Execution Mode (Parallel or Sequential)
# =========================

def calculate_iv(df: pd.DataFrame,
                 target: str,
                 features: Optional[List[str]] = None,
                 alpha: float = 0.5,
                 execution: str = "sequential",  # New argument for execution mode
                 max_workers: int = 4) -> Tuple[pd.DataFrame, pd.DataFrame, Dict]:
    if target not in df.columns:
        raise ValueError(f"Target column '{target}' not found.")

    if len(df[target].unique()) < 2:
        raise ValueError("Target must have at least two classes.")

    features = features or [col for col in df.columns if col != target]

    if execution == "sequential":
        return calculate_iv_sequential(df, target, features, alpha)
    elif execution == "concurrent":
        return calculate_iv_parallel(df, target, features, alpha, max_workers)
    else:
        raise ValueError("Execution mode must be either 'sequential' or 'concurrent'")


# =========================
# Sequential IV Function
# =========================
def calculate_iv_sequential(df: pd.DataFrame,
                            target: str,
                            features: Optional[List[str]] = None,
                            alpha: float = 0.5) -> Tuple[pd.DataFrame, pd.DataFrame, Dict]:

    if target not in df.columns:
        raise ValueError(f"Target column '{target}' not found.")

    if len(df[target].unique()) < 2:
        raise ValueError("Target must have at least two classes.")

    features = features or [col for col in df.columns if col != target]

    all_bin_stats = []
    woe_maps = {}

    for feature in features:
        if pd.api.types.is_numeric_dtype(df[feature]) and df[feature].nunique() > 2:
            bin_stats, woe_map = mono_bin(df[target], df[feature], var_name=feature, alpha=alpha)
        else:
            bin_stats, woe_map = char_bin(df[target], df[feature], var_name=feature, alpha=alpha)

        all_bin_stats.append(bin_stats)
        woe_maps[feature] = woe_map

    all_stats_df = pd.concat(all_bin_stats, ignore_index=True)

    iv_summary = all_stats_df.groupby('VAR_NAME').agg(
        IV=('IV', 'sum'),
        BINS=('VAR_NAME', 'count')
    ).reset_index().rename(columns={'VAR_NAME': 'VARIABLE'})

    iv_summary['STRENGTH'] = pd.cut(
        iv_summary['IV'],
        bins=[-np.inf, 0.02, 0.1, 0.3, np.inf],
        labels=['Useless', 'Weak', 'Medium', 'Strong']
    )

    # Apply WOE values
    df_woe = df.copy()
    for feature, woe_map in woe_maps.items():
        if pd.api.types.is_numeric_dtype(df[feature]):
            def apply_numeric_woe(val):
                if pd.isna(val):
                    return woe_map.get(np.nan, 0)
                for (low, high), woe in woe_map.items():
                    if isinstance((low, high), tuple):
                        if low <= val <= high:
                            return woe
                return 0  # fallback if no bin matches

            df_woe[f'{feature}_WOE'] = df[feature].apply(apply_numeric_woe)
        else:
            df_woe[f'{feature}_WOE'] = df[feature].map(woe_map)

    return iv_summary.sort_values('IV', ascending=False), df_woe, woe_maps




# =========================
# Parallel IV Function
# =========================
def calculate_iv_parallel(df: pd.DataFrame,
                          target: str,
                          features: Optional[List[str]] = None,
                          alpha: float = 0.5,
                          max_workers: Optional[int] = None) -> Tuple[pd.DataFrame, pd.DataFrame, Dict]:
    """
    Calculates IV and WOE values in parallel using threading.
    """
    if target not in df.columns:
        raise ValueError(f"Target column '{target}' not found.")

    if len(df[target].unique()) < 2:
        raise ValueError("Target must have at least two classes.")

    features = features or [col for col in df.columns if col != target]

    all_bin_stats = []
    woe_maps = {}

    with ThreadPoolExecutor(max_workers=max_workers or 4) as executor:
        futures = [executor.submit(_iv_worker, (df, target, feature, alpha)) for feature in features]

        for future in as_completed(futures):
            try:
                feature, bin_stats, woe_map = future.result()
                all_bin_stats.append(bin_stats)
                woe_maps[feature] = woe_map
            except Exception as e:
                print(f"Failed to process feature in parallel: {e}")

    # Combine all bin stats
    all_stats_df = pd.concat(all_bin_stats, ignore_index=True)

    # Summary IV
    iv_summary = all_stats_df.groupby('VAR_NAME').agg(
        IV=('IV', 'sum'),
        BINS=('VAR_NAME', 'count')
    ).reset_index().rename(columns={'VAR_NAME': 'VARIABLE'})

    iv_summary['STRENGTH'] = pd.cut(
        iv_summary['IV'],
        bins=[-np.inf, 0.02, 0.1, 0.3, np.inf],
        labels=['Useless', 'Weak', 'Medium', 'Strong']
    )

    # Apply WOE transformation
    df_woe = df.copy()
    for feature, woe_map in woe_maps.items():
        if pd.api.types.is_numeric_dtype(df[feature]):
            def apply_numeric_woe(val):
                if pd.isna(val):
                    return woe_map.get(np.nan, 0)
                for (low, high), woe in woe_map.items():
                    if isinstance((low, high), tuple) and low <= val <= high:
                        return woe
                return 0
            df_woe[f'{feature}_WOE'] = df[feature].apply(apply_numeric_woe)
        else:
            df_woe[f'{feature}_WOE'] = df[feature].map(woe_map)

    return iv_summary.sort_values('IV', ascending=False), df_woe, woe_maps

# =========================
# Random Forest Feature Importance
# =========================
def calculate_rf_importance(df, target, features):
    # Separate target variable
    X = df[features]
    y = df[target]
    
    # Preprocess the data (Handle missing values and encode categorical features)
    preprocessor = ColumnTransformer(
        transformers=[
            # Numerical features: Impute missing values with the mean
            ('num', SimpleImputer(strategy='mean'), X.select_dtypes(include=['float64', 'int64']).columns),
            
            # Categorical features: Impute missing values with the most frequent value, then one-hot encode
            ('cat', Pipeline([
                ('imputer', SimpleImputer(strategy='most_frequent')),  # Impute categorical data with most frequent value
                ('encoder', OneHotEncoder(handle_unknown='ignore'))  # One-hot encode categorical data
            ]), X.select_dtypes(include=['object']).columns)
        ]
    )
    
    # Create a pipeline with preprocessing and the random forest classifier
    rf_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('rf', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    
    # Fit the model
    rf_pipeline.fit(X, y)
    
    # Get feature importance
    feature_importances = rf_pipeline.named_steps['rf'].feature_importances_
    
    # Get the transformed feature names after encoding
    # We will extract the feature names from the OneHotEncoder
    feature_names = rf_pipeline.named_steps['preprocessor'].transformers_[1][1].named_steps['encoder'].get_feature_names_out(X.select_dtypes(include=['object']).columns)
    
    # Combine numerical and categorical feature names
    all_feature_names = list(X.select_dtypes(include=['float64', 'int64']).columns) + list(feature_names)
    
    # Create a DataFrame to show feature importances
    importance_df = pd.DataFrame({
        'Feature': all_feature_names,
        'Importance': feature_importances
    }).sort_values(by='Importance', ascending=False)
    
    return importance_df



# Helper function to compute feature importance for one feature
def compute_feature_importance(X, y, feature, preprocessor):
    """
    Computes the RandomForest feature importance for a given feature with pre-processing.
    """
    X_feature = X[[feature]]  # Select only the current feature
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('rf', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    pipeline.fit(X_feature, y)
    return feature, pipeline.named_steps['rf'].feature_importances_


def calculate_rf_importance_concurrent(df: pd.DataFrame, target: str, features: List[str], max_workers: int = 4) -> pd.DataFrame:
    """
    Calculate RandomForest feature importances concurrently.
    """
    # Separate target and feature matrix
    X = df[features]
    y = df[target]
    
    # Preprocessing: Handle missing values and encode categorical features
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', SimpleImputer(strategy='mean'), X.select_dtypes(include=['float64', 'int64']).columns),
            ('cat', Pipeline([
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('encoder', OneHotEncoder(handle_unknown='ignore', sparse=False))
            ]), X.select_dtypes(include=['object']).columns)
        ]
    )

    # Use ThreadPoolExecutor for concurrent execution
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        # Submit tasks for each feature
        for feature in features:
            futures.append(executor.submit(compute_feature_importance, X, y, feature, preprocessor))
        
        # Collect results as they finish
        results = []
        for future in as_completed(futures):
            feature, importance = future.result()
            results.append((feature, importance))

    # Create a DataFrame to store feature importances
    importance_df = pd.DataFrame(results, columns=['Feature', 'Importance'])
    importance_df['Importance'] = importance_df['Importance'].apply(lambda x: x[0])  # Extract single value from list
    importance_df = importance_df.sort_values(by='Importance', ascending=False)

    return importance_df

