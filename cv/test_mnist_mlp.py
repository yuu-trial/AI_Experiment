
import argparse
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from PIL import Image

from network import MLP

def main():
	parser = argparse.ArgumentParser(description='Pytorch example: CIFAR-10')
	parser.add_argument('--gpu', '-g', type=int, default=-1,
						help='GPU ID (negative value indicates CPU)')
	parser.add_argument('--model', '-m', default='result/model_final',
						help='Path to the model for test')
	parser.add_argument('--image', '-i', default='image.png',
						help='Path to the model for test')
	parser.add_argument('--unit', '-u', type=int, default=1000,
						help='Number of units')
	args = parser.parse_args()

	print('GPU: {}'.format(args.gpu))
	print('')

	# Set up a neural network to test
	net = MLP(args.unit, 28*28, 10)
	# Load designated network weight 
	net.load_state_dict(torch.load(args.model))
	# Set model to GPU
	device = 'cpu'
	if args.gpu >= 0:
		# Make a specified GPU current
		device = 'cuda:' + str(args.gpu)
		net = net.to(device)

	# Load image
	transform = transforms.Compose(	[
		transforms.Grayscale(),
		transforms.Resize((28, 28)),
		transforms.ToTensor()] )
	image = transform(Image.open(args.image, 'r')).unsqueeze(0).to(device)

	with torch.no_grad():
		# Reshape the input
		image = image.view(-1, 28*28)
		if args.gpu >= 0:
			image = image.to(device)
		# Forward
		outputs = net(image)
		# Predict the label
# 		_, predicted = torch.max(outputs, 1)
		_, predicted = torch.topk(outputs, 3)
		# Print the result
		print('Predicted label : {0}, {1}, {2}'.format(predicted[0][0].tolist(),predicted[0][1].tolist(),predicted[0][2].tolist()))

if __name__ == '__main__':
	main()
