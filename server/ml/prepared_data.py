import numpy as np
import math
import pandas as pd


def prepared_data(df: pd.DataFrame, num_pass: float = 0.7) -> pd.DataFrame:
    """Очистка и подготовка входного DataFrame

    Args:
        df (pd.DataFrame): Входной DataFrame, содержащий исходные данные.
        num_pass (float, optional): Количество пропусков в датафрейме. 
                                    По умолчанию 0.7.

    Returns:
        pd.DataFrame: Очищенный и подготовленный DataFrame.
    """
    df = df.dropna(subset=['cap-diameter', 'stem-height', 'stem-width'])
    if len(df) > 12_000:
        df = df.sample(n=12_000, random_state=42)
    # удаляем лишние столбцы и столбцы с большим количеством пропусков
    df = df.drop(columns=["id"], errors='ignore')
    df = df[[col for col in df if df[col].count() / len(df) >= num_pass]]
    # уменьшаем количество категорий по каждому признаку, собирая все небольшие категории в одну
    df['cap-shape'] = np.where(
        df['cap-shape'].isin(['s', 'o', 'f', 'b', 'x', 'c', 'p']), df['cap-shape'], 'oth')
    df['habitat'] = np.where(df['habitat'].isin(["d", "g"]), df['habitat'], 'o')
    df['ring-type'] = np.where(df['ring-type'] != "f", "o", df['ring-type'])
    df['stem-color'] = np.where(df['stem-color'].isin(["n", "w", "y"]), df['stem-color'], 'oth')
    df['does-bruise-or-bleed'] = np.where(
        df['does-bruise-or-bleed'].isin(["t", "f"]), df['does-bruise-or-bleed'], 'oth')
    df['has-ring'] = np.where(df['has-ring'].isin(["t", "f"]), df['has-ring'], 'oth')
    df['gill-color'] = np.where(
        df['gill-color'].isin(["n", "w", "y", "b", "p", "g", "e", "o"]), df['gill-color'], 'oth')
    df['gill-attachment'] = np.where(
        df['gill-attachment'].isin(["a", "e", "p", "x", "d", "s"]), df['gill-attachment'], 'oth')
    df['cap-color'] = np.where(
        df['cap-color'].isin(["n", "w", "y", "b", "p", "g", "e", "o"]), df['cap-color'], 'oth')
    df['cap-surface'] = np.where(
        df['cap-surface'].isin(["t", "d", "h", "s", "y", "k", "g"]), df['cap-surface'], 'oth')
    # считаем площадь гриба и удаляем категории уже исп.категории
    df['square-mushroom'] = round(math.pi * pow((df['cap-diameter'] / 2), 2) + 
                                  df['stem-height'] * df['stem-width'], 2)
    df = df.drop(columns=['cap-diameter', 'stem-height', 'stem-width'], errors='ignore')
    return df