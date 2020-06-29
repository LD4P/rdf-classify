"""FastAI extended data_block"""

import pandas as pd  # type: ignore
from fastai.tabular import Categorify, DataBunch, TabularList  # type: ignore


def databunch(df: pd.DataFrame,
              dependent_var: str = 'resource_template') -> DataBunch:
    # Resource_template is what we're trying to predict
    category_names = ['subject', 'group']
    procedures = [Categorify]
    # All predicates in graph
    continous_names = list(df.keys())[3:]
    # Reserve last 20% of Data Frame for validation
    total = len(df)
    last_start = total - int(total*.2)
    test = TabularList.from_df(df[last_start:total].copy(),
                               cat_names=category_names,
                               cont_names=continous_names)
    return (TabularList.from_df(df,
                                cat_names=category_names,
                                cont_names=continous_names,
                                procs=procedures)
                       .split_by_idx(list(range(last_start, total)))
                       .label_from_df(cols=dependent_var)
                       .add_test(test)
                       .databunch())
