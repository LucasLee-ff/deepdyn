import os

sep = os.sep

DRIVE = {
    'Params': {
        'previous_visit': 4,
        'num_channels': 10,
        'num_classes': 1,
        'batch_size': 16,
        'epochs': 1,
        'learning_rate': 0.001,
        'patch_shape': (61, 61),
        'use_gpu': True,
        'distribute': False,
        'shuffle': True,
        'log_frequency': 200,
        'validation_frequency': 1,
        'mode': 'train',
        'parallel_trained': False
    },
    'Dirs': {
        'image': 'data' + sep + 'DRIVE-TRACKNET' + sep + 'mats',
        'mask': 'data' + sep + 'DRIVE-TRACKNET' + sep + 'mask',
        'logs': 'data' + sep + 'DRIVE-TRACKNET' + sep + 'tracknet_logs',
        'splits_json': 'data' + sep + 'DRIVE-TRACKNET' + sep + 'tracknet_splits'
    },

    'Funcs': {
        'truth_getter': lambda file_name: file_name.split('.')[0] + '_manual1.gif',
        'mask_getter': lambda file_name: file_name.split('.')[0].split('_')[-1] + '_test_mask.gif'
    }
}

DRIVEa = {
    'Params': {
        'num_channels': 1,
        'num_classes': 2,
        'batch_size': 16,
        'epochs': 20,
        'learning_rate': 0.001,
        'patch_shape': (41, 41),
        'use_gpu': True,
        'distribute': False,
        'shuffle': True,
        'log_frequency': 200,
        'validation_frequency': 1,
        'mode': 'train',
        'parallel_trained': False
    },
    'Dirs': {
        'image': 'data' + sep + 'DRIVE-TRACKNET' + sep + 'mats',
        'mask': 'data' + sep + 'DRIVE-TRACKNET' + sep + 'mask',
        'logs': 'data' + sep + 'DRIVE-TRACKNET' + sep + 'tracknet_logs_41',
        'splits_json': 'data' + sep + 'DRIVE-TRACKNET' + sep + 'tracknet_splits'
    },

    'Funcs': {
        'truth_getter': lambda file_name: file_name.split('.')[0] + '_manual1.gif',
        'mask_getter': lambda file_name: file_name.split('.')[0].split('_')[-1] + '_test_mask.gif'
    }
}