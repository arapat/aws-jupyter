#!/usr/bin/python3
import tmsn
import socket
from os.path import expanduser
from time import sleep


class Logger:
    def __init__(self, filename):
        self._file = open(filename, "w")

    def write(self, msg):
        print(msg)
        self._file.write(msg + '\n')


class Message:
    def __init__(self, host_name, num):
        self.num = num
        # fix the length of the host name
        self.host_name = (host_name + '_' * 16)[:16]

    def __bytes__(self):
        return bytes("{},{}".format(self.host_name, self.num), "UTF-8")

    def decode(message):
        if type(message) is list:
            message = bytes(message)
        if type(message) is bytes:
            message = message.decode()
        host_name, num = message.split(',')
        return Message(host_name, int(num))


def get_network():
    host_name = socket.gethostname()
    neighbor_path = "./neighbors.txt"
    with open(neighbor_path) as f:
        neighbors = []
        for line in f.readlines():
            line = line.strip()
            try:
                socket.inet_aton(line)  # valid ip address
                neighbors.append(line)
            except:
                pass
    return (host_name, neighbors)


def main():
    logger = Logger("network.log")
    host_name, neighbors = get_network()
    logger.write("Hostname: {}".format(host_name))
    logger.write("Number of neighbors: {}".format(len(neighbors)))
    network = tmsn.start_network(host_name, neighbors, 8080)
    logger.write("starting the network at the port 8080")
    # wait 3 seconds for network to be established
    sleep(3)

    # Send out first batch of data, a number 0 (or can be any other thing)
    message = bytes(Message(host_name, 0))
    network.send(message)
    logger.write(f"{host_name} just sent '0'")

    # now we try to receive it, update it, and broadcast the new value
    loop = 0
    while loop < 10:
        logger.write('-' * 10)
        ret = network.recv()
        iters = 0
        while not ret and iters < 10:
            iters += 1
            logger.write("Trial {}: No message received, wait 0.5 second.".format(iters))
            sleep(0.5)
            # try again
            ret = network.recv()
        if ret is None:
            logger.write("Failed to receive any message after trying 10 times. Exit.")
            sys.exit(1)
        incoming = Message.decode(ret)
        source, number = incoming.host_name, incoming.num
        logger.write(f"Trial {iters + 1}: Message received from {source}. Message is '{number}'.")
        new_message = bytes(Message(host_name, number + 1))
        network.send(new_message)
        logger.write(f"{host_name} just sent '{number + 1}'")
        loop += 1
    logger.write("Exit with no error.")


if __name__ == '__main__':
    main()

