import argparse
import RDT
import time

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Quotation client talking to a Pig Latin server.')
    parser.add_argument('server', help='Server.')
    parser.add_argument('port', help='Port.', type=int)
    args = parser.parse_args()

    msg_L = ['The use of COBOL cripples the mind; its teaching should, therefore, be regarded as a criminal offense. -- Edsgar Dijkstra',
            'C makes it easy to shoot yourself in the foot; C++ makes it harder, but when you do, it blows away your whole leg. -- Bjarne Stroustrup',
            'A mathematician is a device for turning coffee into theorems. -- Paul Erdos',
            'Grove giveth and Gates taketh away. -- Bob Metcalfe (inventor of Ethernet) on the trend of hardware speedups not being able to keep up with software demands',
            'Wise men make proverbs, but fools repeat them. -- Samuel Palmer (1805-80)']

    # send the next message if no response
    timeout = 2
    time_of_last_data = time.time()

    rdt = RDT.RDT('client', args.server, args.port)
    for msg_S in msg_L:
        #print('Converting using RDT1.0: '+msg_S)
        #rdt.rdt_1_0_send(msg_S)
        print('Converting using RDT2.1: '+msg_S)
        rdt.rdt_2_1_send(msg_S)
        # TODO Implement other RDT .send()
        # print('Converting using RDT2.1: '+msg_S)
        # rdt.rdt_2_1_send(msg_S)
        # print('Converting using RDT3.0: '+msg_S)
        # rdt.rdt_3_0_send(msg_S)
        # try to receive message before timeout

        msg_S = None
        while msg_S is None:
            #msg_S = rdt.rdt_1_0_receive()
            msg_S = rdt.rdt_2_1_receive()
            # TODO implement other RDT .receive()
            # msg_S = rdt.rdt_2_1_receive()
            # msg_S = rdt.rdt_3_0_receive()

            if msg_S is None:
                if time_of_last_data + timeout < time.time():
                    break
                else:
                    continue
        time_of_last_data = time.time()

        # print the result
        if msg_S:
            print('to: '+msg_S+'\n')
    rdt.disconnect()
