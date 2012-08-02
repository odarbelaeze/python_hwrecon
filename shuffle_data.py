#!/usr/bin/env python

import random

def main():
	f = open("char_recon.db")
	lines = f.readlines()
	f.close()
	random.shuffle(lines)
	f = open("char_recon_shuffled.db", 'w')
	f.writelines(lines)
	f.close()

if __name__ == '__main__':
	main()