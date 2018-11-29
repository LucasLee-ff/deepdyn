"""
### author: Aashis Khanal
### sraashis@gmail.com
### date: 9/10/2018
"""

import os
import traceback

import torch
import torch.optim as optim
import torchvision.transforms as transforms

import neuralnet.tracknet.runs as rs
from neuralnet.tracknet.model import TrackNet
from neuralnet.tracknet.tracknet_dataloader import PatchesGenerator
from neuralnet.tracknet.tracknet_trainer import TracknetTrainer
from neuralnet.utils import auto_split as asp
import neuralnet.utils.nviz as plt

RUNS = [rs.DRIVE]


def main():
    transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.ToTensor()
    ])

    for R in RUNS:
        for k, folder in R['Dirs'].items():
            os.makedirs(folder, exist_ok=True)

        for split in os.listdir(R['Dirs']['splits_json']):
            splits = asp.load_split_json(os.path.join(R['Dirs']['splits_json'], split))

            R['checkpoint_file'] = split + '.tar'
            model = TrackNet(R['Params']['num_channels'], R['Params']['num_classes'])
            optimizer = optim.Adam(model.parameters(), lr=R['Params']['learning_rate'])
            if R['Params']['distribute']:
                model = torch.nn.DataParallel(model)
                model.float()
                optimizer = optim.Adam(model.module.parameters(), lr=R['Params']['learning_rate'])

            try:
                drive_trainer = TracknetTrainer(model=model, run_conf=R)

                if R.get('Params').get('mode') == 'train':
                    train_loader = PatchesGenerator.get_loader(run_conf=R, images=splits['train'], transforms=transform,
                                                               mode='train')
                    val_loader = PatchesGenerator.get_loader_per_img(run_conf=R, images=splits['validation'],
                                                                     mode='validation')
                    drive_trainer.train(optimizer=optimizer, data_loader=train_loader, validation_loader=val_loader)

                drive_trainer.resume_from_checkpoint(parallel_trained=R.get('Params').get('parallel_trained'))
                test_loader = PatchesGenerator.get_loader_per_img(run_conf=R,
                                                                  images=splits['test'], mode='test')

                logger = drive_trainer.get_logger(drive_trainer.test_log_file,
                                                  header='ID,LOSS')
                drive_trainer.evaluate(data_loaders=test_loader, logger=logger, gen_images=True)
                # plt.plot(file=drive_trainer.test_log_file, y='LOSS', title='Test', x_tick_skip=len(val_loader),
                #          save=True)
                logger.close()
            except Exception as e:
                traceback.print_exc()


if __name__ == "__main__":
    main()
