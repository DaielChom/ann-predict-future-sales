import pandas as pd

def load_dataset(dataset_dir):
    
    items = pd.read_csv(dataset_dir+"items.csv")
    dataset = pd.read_csv(dataset_dir+"sales_train.csv")

    # get categories data
    categories = dict(items[["item_id", "item_category_id"]].values)
    get_category = lambda x: categories[x]
    dataset["item_category_id"] = dataset.item_id.apply(get_category)

    # fix date index
    dataset["date"] = pd.to_datetime([pd.Timestamp(i).date() for i in pd.to_datetime(dataset.date, format="%d.%M.%Y").values])
    _ = dataset.pop("date_block_num")

    return dataset