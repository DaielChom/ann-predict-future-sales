import pandas as pd

shops_to_use = [ 2,  3,  4,  5,  6,  7, 10, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 24, 25, 26, 27, 28, 29, 30, 31, 35, 37, 38, 39, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59]
items_to_use = [32,  33,  464,  482,  485,  492,   687, 806, 839, 972, 1007, 1201, 1249, 1460, 1467, 1471, 1481, 1495, 1523,
 1830, 1855, 1856, 1857, 1905, 1915, 1916, 1921, 2252, 2267, 2269, 2308, 2416, 2445, 2574, 2607, 2678, 2703, 2753, 2808, 2854, 2921, 2946, 3007, 3076, 3077, 3141, 3148, 3183, 3320, 3325, 3328,
 3329, 3331, 3335, 3423, 3475, 3476, 3554, 3556, 3656, 3676, 3686, 3689, 3695, 3708, 3719, 3732, 3734, 3851, 4178, 4181, 4228, 4231, 4233, 4240, 4244, 4248, 4249, 4251, 4351, 4477, 4779, 4806,
 4870, 4885, 4886, 4901, 4904, 4906, 4907, 5035, 5036, 5060, 5260, 5272, 5275, 5324, 5361, 5380, 5459, 5572, 5583, 5643, 5655, 5660, 5663, 5672, 5811, 5820, 5821, 5822, 5823, 5946, 6005, 6090,
 6121, 6156, 6185, 6457, 6466, 6472, 6482, 6488, 6490, 6495, 6497, 6498, 6501, 6675, 6717, 6738, 6740, 6911, 7070, 7071, 7072, 7202, 7213, 7215, 7220, 7736, 7770, 7812, 7815, 7856, 7860, 7872,
 7893, 7894, 7895, 7912, 7956, 8093, 8686, 8778, 8863, 9507, 9871, 10292, 10298, 10331, 10659, 11370, 11389, 11391, 11496, 11655, 11711, 11811, 11921, 12134, 12135, 12361, 12472, 12550, 12552, 12828, 12860, 13071,
 13851, 13881, 13923, 14019, 14227, 14228, 14229, 14432, 14447, 14829, 14842, 14931, 15016, 15031, 15044, 15045, 15063, 15256, 15284, 15446, 15470, 15833, 15836, 16011, 16014, 16020, 16056, 16071, 16167, 16169, 16182,
 16184, 16205, 16206, 16209, 16210, 16227, 16315, 16450, 16787, 17717, 19597, 19602, 19860, 20231, 20606, 20607, 20608, 20609, 20610, 20949, 21377, 21404, 21427, 21440, 21488, 21876, 21880, 22076, 22087, 22088, 22091, 22092,
 22167]


def load_dataset(dataset_dir):
    
    items = pd.read_csv(dataset_dir+"items.csv")
    dataset = pd.read_csv(dataset_dir+"sales_train.csv")

    # get categories data
    categories = dict(items[["item_id", "item_category_id"]].values)
    get_category = lambda x: categories[x]
    dataset["item_category_id"] = dataset.item_id.apply(get_category)

    # fix date index
    dataset["date"] = pd.to_datetime([pd.Timestamp(i).date() for i in pd.to_datetime(dataset.date, format="%d.%m.%Y").values])
    _ = dataset.pop("date_block_num")

    return dataset

def get_base_dataset(dataset_dir):
    
    # read base dataset
    shop_item = pd.read_csv(dataset_dir+"base_dataset.csv", index_col=0)
    shop_item = shop_item.fillna(0)

    # get signals
    signals = shop_item.columns.tolist()

    return shop_item, signals

def get_split_signal_data(signal, month_to_predict, look_back, dataset_dir, reshape=True):

    # get signal data
    shop_item, _ = get_base_dataset(dataset_dir)
    signal_data = shop_item[[signal]]

    # building dataset
    columns = []
    for i in [i for i in range(look_back-1)][::-1]:
        
        columns.append(signal+"-{}".format(i+1))
        signal_data[signal+"-{}".format(i+1)] = signal_data[signal].shift(i+1)
    columns.append(signal)

    signal_data["target"] = signal_data[signal].shift(-1)
    signal_data = signal_data.dropna()

    # split dataset
    train = signal_data[:-month_to_predict]
    test = signal_data[-month_to_predict:]

    X_train = train[columns].values
    y_train = train["target"].values
    i_train = train.index.tolist()

    X_test = test[columns].values
    y_test = test["target"].values
    i_test = test.index.tolist()
    
    if reshape:
        X_train = X_train.reshape((X_train.shape[0], 1, X_train.shape[1]))
        y_train = y_train.reshape((y_train.shape[0], 1))

        X_test = X_test.reshape((X_test.shape[0], 1, X_test.shape[1]))
        y_test = y_test.reshape((y_test.shape[0], 1))

    return X_train, y_train, i_train, X_test, y_test, i_test






