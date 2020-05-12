from Queue.arrays import Array
from Queue.arrayqueue import ArrayQueue
from simplepeople import Passenger, TicketAgent
import random
random.seed(4500)


class TicketCounterSimulation:
    def __init__(self, numAgents, numMinutes, betweenTime, serviceTime):
        self._arriveProb = 1.0 / betweenTime
        self._serviceTime = serviceTime
        self._numMinutes = numMinutes

        self._passengerQ = ArrayQueue()
        self._theAgents = Array(numAgents)
        for i in range(numAgents):
            self._theAgents[i] = TicketAgent(i + 1)

        self._numAgents = numAgents

        self._totalWaitTime = 0
        self._numPassengers = 0

    # Run the simulation using the parameters supplied earlier.
    def run(self):
        for curTime in range(self._numMinutes + 1):
            # print(f'time {curTime}:')
            self._handleArrival(curTime)
            self._handleBeginService(curTime)
            self._handleEndService(curTime)

    def _handleArrival(self, curTime):
        """
        Decides whether a passanger comes on this day
        and handles it
        :param curTime: int
        :return: None
        """
        if random.random() <= self._arriveProb:
            # print(f'passenger {self._numPassengers + 1}')
            self._passengerQ.add(Passenger(self._numPassengers, curTime))
            self._numPassengers += 1

    def _handleBeginService(self, Curtime):
        """
        Occupies all the agent with work
        :param Curtime: int
        :return: None
        """
        while len(self._passengerQ) > 0:
            for i in range(self._numAgents):
                if self._theAgents[i].isFree():
                    passenger = self._passengerQ.pop()
                    self._theAgents[i].startService(passenger, Curtime +
                                                    self._serviceTime)
                    # print(f'Agent {i+ 1} took {passenger.idNum() + 1}')
                    break
            break
        self._totalWaitTime += len(self._passengerQ)

    def _handleEndService(self, curTime):
        """
        reads through all of the agents and checks if
        they satisfied their clients.
        :param curTime: int
        :return: None
        """
        for i in range(self._numAgents):
            if self._theAgents[i].isFree():
                continue
            elif self._theAgents[i].isFinished(curTime):
                self._theAgents[i].stopService()
                # print(f'Agent {i + 1} stopped')
        # print('WAITING', len(self._passengerQ))

    def printResuts(self):
        numServed = self._numPassengers - len(self._passengerQ)
        avgWait = float(self._totalWaitTime) / numServed
        print()
        print("Number of passengers served = ", numServed)
        print("Number of passengers remaining in line = %d" %
              len(self._passengerQ))
        print("The average wait time was %4.2f minutes." % avgWait)


if __name__ == '__main__':
    my_simulation = TicketCounterSimulation(2, 25, 2, 3)
    my_simulation.run()
    my_simulation.printResuts()
