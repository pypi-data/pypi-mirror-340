import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class Datalitex:
    def __init__(self, filepath_or_df):
        print("Datalitex: Smart Data Assistant Initialized.")
        if isinstance(filepath_or_df, str):
            self.df = pd.read_csv(filepath_or_df)
            print("CSV file loaded successfully.")
        elif isinstance(filepath_or_df, pd.DataFrame):
            self.df = filepath_or_df.copy()
            print("DataFrame loaded successfully.")
        else:
            raise ValueError("Input must be a CSV file path or a pandas DataFrame.")
    def head(self, n=5):
        print(f"\n Showing top {n} rows:")
        print(self.df.head(n))
        return self.df.head(n)

    def tail(self, n=5):
        print(f"\n Showing bottom {n} rows:")
        print(self.df.tail(n))
        return self.df.tail(n)
    def show_rows(self, start=0, end=5):
        print(f"\n Showing rows from index {start} to {end}:")
        print(self.df.iloc[start:end])
        return self.df.iloc[start:end]
    def show_all(self):
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print("\n Full Dataset View:")
            print(self.df)
        return self.df

    # ==== Cleaning & Handling ====
    def clean(self):
        print("\n Starting data cleaning...")
        original_cols = self.df.columns.tolist()
        self.df.columns = self.df.columns.str.strip()
        if original_cols != self.df.columns.tolist():
            print(f"Stripped whitespace from column names: {original_cols}")
        
        null_cols = self.df.columns[self.df.isnull().all()].tolist()
        self.df.drop(columns=null_cols, inplace=True)
        if null_cols:
            print(f"Dropped completely null columns: {null_cols}")

        null_rows = self.df.isnull().all(axis=1).sum()
        if null_rows:
            self.df.dropna(how='all', inplace=True)
            print(f"Dropped {null_rows} fully null row(s)")

        numeric_cols = self.df.select_dtypes(include=np.number).columns
        self.df[numeric_cols] = self.df[numeric_cols].fillna(self.df[numeric_cols].mean())
        print("Filled missing values with column means.")
        print(f"Shape of Data: {self.df.shape}")

    def handle_duplicates(self, drop=True, subset=None):
        count = self.df.duplicated(subset=subset).sum()
        if drop:
            self.df.drop_duplicates(subset=subset, inplace=True)
            print(f"Dropped {count} duplicate row(s).")
        else:
            print(f"Found {count} duplicate row(s).")

    def summarize(self):
        print(f"\n Shape: {self.df.shape}")
        print("\n Column Data Types:")
        print(self.df.dtypes)
        print("\n Missing Values:")
        print(self.df.isnull().sum())
        print("\n Descriptive Statistics:")
        print(self.df.describe(include='all'))

    # ==== Transformation & Manipulation ====
    def filter_rows(self, condition_func):
        filtered = self.df[condition_func(self.df)]
        print(f"\n Filtered rows: {filtered.shape[0]} matched.")
        return filtered

    def query(self, expr):
        try:
            result = self.df.query(expr)
            print(f"\n Query matched {len(result)} rows.")
            return result
        except Exception as e:
            print(f"Query error: {e}")
            return pd.DataFrame()

    def convert_dtypes(self, dtype_map):
        for col, dtype in dtype_map.items():
            if col in self.df.columns:
                try:
                    self.df[col] = self.df[col].astype(dtype)
                    print(f"Converted {col} to {dtype}")
                except Exception as e:
                    print(f"Failed to convert {col}: {e}")

    def parse_dates(self, columns):
        for col in columns:
            if col in self.df.columns:
                try:
                    self.df[col] = pd.to_datetime(self.df[col])
                    print(f"Parsed {col} to datetime.")
                except Exception as e:
                    print(f"Failed to parse {col}: {e}")

    def reorder_columns(self, new_order):
        if set(new_order).issubset(self.df.columns):
            self.df = self.df[new_order + [col for col in self.df.columns if col not in new_order]]
            print(f"Reordered columns as per: {new_order}")
        else:
            print("Invalid reorder request: Some columns not in DataFrame.")

    def drop_columns(self, cols):
        existing = [c for c in cols if c in self.df.columns]
        self.df.drop(columns=existing, inplace=True)
        print(f"Dropped columns: {existing}")

    def drop_rows(self, indices):
        existing = [i for i in indices if i in self.df.index]
        self.df.drop(index=existing, inplace=True)
        print(f"Dropped rows at indices: {existing}")

    def rename_columns(self, rename_dict):
        self.df.rename(columns=rename_dict, inplace=True)
        print(f"Renamed columns: {rename_dict}")

    def rename_index(self, rename_dict):
        self.df.rename(index=rename_dict, inplace=True)
        print(f"Renamed indices: {rename_dict}")

    def add_column(self, col_name, default_value=np.nan):
        self.df[col_name] = default_value
        print(f"Added column: {col_name} with default: {default_value}")

    def add_row(self, row_dict):
        new_row = pd.DataFrame([row_dict])
        self.df = pd.concat([self.df, new_row], ignore_index=True)
        print(" Added new row.")

    # ==== Visualization ====
    def plot_distribution(self, column):
        if column in self.df.columns:
            plt.figure(figsize=(8, 5))
            sns.histplot(self.df[column], kde=True, bins=30)
            plt.title(f"Distribution Plot of {column}")
            plt.show()

    def plot_box(self, column):
        if column in self.df.columns:
            plt.figure(figsize=(6, 4))
            sns.boxplot(x=self.df[column])
            plt.title(f"Boxplot of {column}")
            plt.show()

    def plot_bar(self, column):
        if column in self.df.columns:
            plt.figure(figsize=(8, 5))
            self.df[column].value_counts().plot(kind='bar')
            plt.title(f"Bar Plot of {column}")
            plt.ylabel("Count")
            plt.show()

    def plot_heatmap(self):
        plt.figure(figsize=(10, 6))
        sns.heatmap(self.df.corr(numeric_only=True), annot=True, cmap='coolwarm')
        plt.title("Correlation Heatmap")
        plt.show()

    def plot_scatter(self, x, y):
        if x in self.df.columns and y in self.df.columns:
            plt.figure(figsize=(7, 5))
            sns.scatterplot(data=self.df, x=x, y=y)
            plt.title(f"Scatter Plot: {x} vs {y}")
            plt.show()

    def plot_pairplot(self, columns=None):
        cols = columns if columns else self.df.select_dtypes(include=np.number).columns.tolist()
        sns.pairplot(self.df[cols])
        plt.suptitle("Pairplot", y=1.02)
        plt.show()

    def plot_pie(self, column):
        if column in self.df.columns:
            self.df[column].value_counts().plot.pie(autopct='%1.1f%%', figsize=(6, 6))
            plt.title(f"Pie Chart of {column}")
            plt.ylabel('')
            plt.show()

    def plot_line(self, x, y):
        if x in self.df.columns and y in self.df.columns:
            plt.figure(figsize=(8, 5))
            sns.lineplot(data=self.df, x=x, y=y)
            plt.title(f"Line Plot: {y} over {x}")
            plt.show()

    # ==== GroupBy Summary ====
    def groupby_summary(self, by, agg=None):
        if isinstance(by, str):
            by = [by]
        if not all(col in self.df.columns for col in by):
            print(" Invalid group by column(s).")
            return pd.DataFrame()

        try:
            grouped = self.df.groupby(by).agg(agg) if agg else self.df.groupby(by).mean(numeric_only=True)
            print(f"\n Grouped summary by {by}:")
            print(grouped)
            return grouped
        except Exception as e:
            print(f" GroupBy error: {e}")
            return pd.DataFrame()

    # ==== Outlier Detection ====
    def detect_outliers(self, column, method='iqr', z_thresh=3):
        if column not in self.df.columns:
            print(f" Column '{column}' not found in the DataFrame.")
            return pd.DataFrame()

        if method == 'iqr':
            Q1 = self.df[column].quantile(0.25)
            Q3 = self.df[column].quantile(0.75)
            IQR = Q3 - Q1
            outliers = self.df[(self.df[column] < Q1 - 1.5 * IQR) | (self.df[column] > Q3 + 1.5 * IQR)]
        elif method == 'zscore':
            mean = self.df[column].mean()
            std = self.df[column].std()
            z_scores = (self.df[column] - mean) / std
            outliers = self.df[np.abs(z_scores) > z_thresh]
        else:
            print(" Method must be either 'iqr' or 'zscore'")
            return pd.DataFrame()

        print(f" Found {len(outliers)} outliers in column '{column}' using method '{method}'.")
        return outliers

    # ==== Crosstab & Pivot Tables ====
    def get_crosstab(self, col1, col2):
        if col1 in self.df.columns and col2 in self.df.columns:
            ct = pd.crosstab(self.df[col1], self.df[col2])
            print(f"\n Crosstab between '{col1}' and '{col2}':")
            print(ct)
            return ct
        else:
            print(" One or both columns not found.")
            return pd.DataFrame()

    def get_pivot(self, index, columns, values, aggfunc='mean'):
        try:
            pivot = pd.pivot_table(self.df, index=index, columns=columns, values=values, aggfunc=aggfunc)
            print(f"\n Pivot Table with index='{index}', columns='{columns}', values='{values}':")
            print(pivot)
            return pivot
        except Exception as e:
            print(f" Pivot table error: {e}")
            return pd.DataFrame()

    # ==== General Feature Importance ====
    def feature_importance(self, target_column, method='correlation', top_n=10):
        if target_column not in self.df.columns:
            print(f" Target column '{target_column}' not found in the DataFrame.")
            return pd.Series()

        numeric_features = self.df.select_dtypes(include=np.number).drop(columns=[target_column], errors='ignore')

        if method == 'correlation':
            if self.df[target_column].dtype in [np.float64, np.int64]:
                corr = numeric_features.corrwith(self.df[target_column]).abs().sort_values(ascending=False).head(top_n)
                print(f"\n Top {top_n} features correlated with '{target_column}':")
                print(corr)
                return corr
            else:
                print(" Correlation method requires a numeric target column.")
                return pd.Series()

        elif method == 'anova':
            from sklearn.feature_selection import f_classif
            from sklearn.preprocessing import LabelEncoder

            df_copy = self.df.copy()
            for col in df_copy.select_dtypes(include='object').columns:
                df_copy[col] = LabelEncoder().fit_transform(df_copy[col].astype(str))

            X = df_copy.drop(columns=[target_column], errors='ignore').select_dtypes(include=np.number)
            y = df_copy[target_column]

            if y.dtype == 'object':
                y = LabelEncoder().fit_transform(y)

            f_values, p_values = f_classif(X, y)
            importance = pd.Series(f_values, index=X.columns).sort_values(ascending=False).head(top_n)
            print(f"\n Top {top_n} ANOVA F-value features for target '{target_column}':")
            print(importance)
            return importance

        else:
            print(" Unsupported method. Choose 'correlation' or 'anova'.")
            return pd.Series()
    def missing_value_report(self):
        print("\n Missing Value Report (%):")
        missing = self.df.isnull().mean() * 100
        print(missing[missing > 0].sort_values(ascending=False))
        return missing

    # 2. Encode categorical columns using Label Encoding or One-Hot
    def encode_categoricals(self, method='label'):
        cat_cols = self.df.select_dtypes(include='object').columns
        if method == 'label':
            from sklearn.preprocessing import LabelEncoder
            for col in cat_cols:
                self.df[col] = LabelEncoder().fit_transform(self.df[col].astype(str))
            print("Label Encoded categorical columns.")
        elif method == 'onehot':
            self.df = pd.get_dummies(self.df, columns=cat_cols)
            print("One-Hot Encoded categorical columns.")
        else:
            print("Encoding method must be 'label' or 'onehot'.")

    # 3. Remove outliers from a column
    def remove_outliers(self, column, method='iqr', z_thresh=3):
        before = len(self.df)
        outliers = self.detect_outliers(column, method, z_thresh)
        self.df = self.df.drop(outliers.index)
        after = len(self.df)
        print(f"Removed {before - after} outliers from '{column}'.")

    # 4. Normalize numeric features
    def normalize(self, columns=None):
        cols = columns if columns else self.df.select_dtypes(include=np.number).columns
        self.df[cols] = (self.df[cols] - self.df[cols].min()) / (self.df[cols].max() - self.df[cols].min())
        print(f"Normalized columns: {list(cols)}")

    # 5. Standardize numeric features
    def standardize(self, columns=None):
        cols = columns if columns else self.df.select_dtypes(include=np.number).columns
        self.df[cols] = (self.df[cols] - self.df[cols].mean()) / self.df[cols].std()
        print(f"Standardized columns: {list(cols)}")

    # 6. Correlation matrix return
    def get_correlation_matrix(self):
        corr = self.df.corr(numeric_only=True)
        print("\n Correlation Matrix:")
        print(corr)
        return corr

    # 7. Save cleaned/transformed DataFrame to CSV
    def save_to_csv(self, filename):
        self.df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

    # 8. Reset index of DataFrame
    def reset_index(self, drop_old=False):
        self.df.reset_index(drop=drop_old, inplace=True)
        print("Index reset.")

    # 9. Display random sample
    def show_sample(self, n=5):
        sample = self.df.sample(n)
        print(f"\n Showing random sample of {n} rows:")
        print(sample)
        return sample

    # 10. Value counts for a column
    def value_counts(self, column):
        if column in self.df.columns:
            vc = self.df[column].value_counts()
            print(f"\n Value Counts for '{column}':")
            print(vc)
            return vc
        else:
            print("Column not found.")
            return pd.Series()