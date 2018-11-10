import os
import traceback

import torch
import torch.optim as optim
import torchvision.transforms as transforms

from neuralnet.mapnet.mapnet_dataloader import PatchesGenerator
from neuralnet.mapnet.mapnet_trainer import MAPNetTrainer
from neuralnet.mapnet.model import MapUNet
from neuralnet.mapnet.runs import DRIVE, WIDE, STARE, VEVIO
from neuralnet.utils import auto_split as asp

RUNS = [DRIVE, WIDE, STARE, VEVIO]


def main():
    transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.ToTensor()
    ])

    for R in [DRIVE]:
        for k, folder in R['Dirs'].items():
            os.makedirs(folder, exist_ok=True)

        for split in os.listdir(R['Dirs']['splits_json']):
            splits = asp.load_split_json(os.path.join(R['Dirs']['splits_json'], split))
            R['checkpoint_file'] = split + '.tar'

            model = MapUNet(R['Params']['num_channels'], R['Params']['num_classes'])
            optimizer = optim.Adam(model.parameters(), lr=R['Params']['learning_rate'])
            if R['Params']['distribute']:
                model = torch.nn.DataParallel(model)
                model.float()
                optimizer = optim.Adam(model.module.parameters(), lr=R['Params']['learning_rate'])

            try:
                drive_trainer = MAPNetTrainer(model=model, run_conf=R)

                if R.get('Params').get('mode') == 'train':
                    train_loader = PatchesGenerator.get_loader(run_conf=R, images=splits['train'], transforms=transform,
                                                               mode='train')
                    val_loader = PatchesGenerator.get_loader_per_img(run_conf=R, images=splits['validation'],
                                                                     mode='validation')
                    drive_trainer.train(optimizer=optimizer, data_loader=train_loader, validation_loader=val_loader)

                drive_trainer.resume_from_checkpoint(parallel_trained=R.get('Params').get('parallel_trained'))
                test_loader = PatchesGenerator.get_loader_per_img(run_conf=R, images=splits['test'], mode='test')

                logger = drive_trainer.get_logger(drive_trainer.test_log_file,
                                                  header='ID,PRECISION,RECALL,F1,ACCURACY')
                drive_trainer.evaluate(data_loaders=test_loader, logger=logger, gen_images=True)
                logger.close()
                drive_trainer.plot_test(file=drive_trainer.test_log_file)
            except Exception as e:
                traceback.print_exc()


if __name__ == "__main__":
    main()
