import torch
from scipy.io import savemat
from torch.utils.data import DataLoader, ConcatDataset
from torchvision.models.feature_extraction import create_feature_extractor
from tqdm import tqdm

from tools.dataset import CustomValidationDataset


@torch.no_grad()
def feature_extractor(model, loader, device):
    features = []
    labels = []
    model.eval()

    iterator = tqdm(loader)
    for images, batch_labels in iterator:  # 修改变量名
        images = images.to(device)
        feature = model(images)['avgpool_output']
        feature = torch.flatten(feature, 1)

        # 将特征和标签转换为numpy数组并存储
        features_np = feature.cpu().numpy()
        labels_np = batch_labels.cpu().numpy()

        # 追加到列表（保持对应关系）
        features.extend(features_np)
        labels.extend(labels_np)  # 确保标签为整数类型

    label_dict = labels
    lists = sorted(set(label_dict))
    return features, labels, lists


model_path = r'D:\Code\deep-learning-algorithms\KAN\classification\output\best_model.pt'

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = torch.load(model_path, map_location='cpu', weights_only=False).to(device)
return_nodes = {
    'avgpool': 'avgpool_output'
}
model = create_feature_extractor(model, return_nodes=return_nodes)

test_data = CustomValidationDataset(root_dir=r'D:\Code\0-data\3-故障诊断数据集\1-data\test')
val_data = CustomValidationDataset(root_dir=r'D:\Code\0-data\3-故障诊断数据集\1-data\val')
train_data = CustomValidationDataset(root_dir=r'D:\Code\0-data\3-故障诊断数据集\1-data\train')
batch_size = 100
test_dataloader = DataLoader(test_data, batch_size=batch_size, shuffle=False)
val_dataloader = DataLoader(val_data, batch_size=batch_size, shuffle=False)
train_dataloader = DataLoader(train_data, batch_size=batch_size, shuffle=False)
train_features, train_labels, label = feature_extractor(model, train_dataloader, device)
val_features, val_label, _ = feature_extractor(model, val_dataloader, device)
test_features, test_label, _ = feature_extractor(model, test_dataloader, device)
savemat('goog.mat', {'train_features': train_features, 'train_labels': train_labels,
                     'val_features': val_features, 'val_labels': val_label,
                     'test_features': test_features, 'test_labels': test_label,
                     'label': label, 'label_dict': test_data.classes})
