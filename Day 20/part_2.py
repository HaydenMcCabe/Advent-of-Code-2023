from __future__ import annotations
from queue import Queue
from enum import Enum
import re


class PulseVal(Enum):
    LOW = 0
    HIGH = 1

class Pulse:
    def __init__(self, sender: PulseNode, receiver: PulseNode, value: PulseVal) -> None:
        self.sender = sender
        self.receiver = receiver
        self.value = value

class PulseNode:
    def __init__(self) -> None:
        self._outputs = []

    def connect_input(self, object: PulseNode):
        pass

    def connect_output(self, object: PulseNode):
        self._outputs.append(object)

    def handle_pulse(self, sender: PulseNode, pulse: PulseVal) -> [Pulse]:
        return []

# Simply pass any received pulses to every output in order
class Broadcaster(PulseNode):
    def handle_pulse(self, sender: PulseNode, value: PulseVal) -> [Pulse]:
        return_pulses = []
        for output in self._outputs:
            return_pulses.append(Pulse(self, output, value))
        return return_pulses

class FlipFlop(PulseNode):
    def __init__(self) -> None:
        super().__init__()
        self._stored_value: bool = False

    def handle_pulse(self, sender: PulseNode, value: PulseVal) -> [Pulse]:
        # Toggle and broadcast on low pulses
        if value == PulseVal.LOW:
            self._stored_value = not self._stored_value
            return_pulses = []
            for output in self._outputs:
                return_pulses.append(Pulse(self, output, \
                    PulseVal.HIGH if self._stored_value else PulseVal.LOW))
            return return_pulses
        else:
            return []
        
class Conjunction(PulseNode):
   
    def __init__(self) -> None:
        super().__init__()
        self._input_values = [PulseVal]
        self._input_objects: {PulseNode: int} = {}

    def connect_input(self, object: PulseNode):
        new_input_index = len(self._input_values)
        self._input_values.append(PulseVal.LOW)
        self._input_objects[object] = new_input_index

    def handle_pulse(self, sender: PulseNode, value: PulseVal) -> [Pulse]:
        input_index = self._input_objects[sender]
        self._input_values[input_index] = value
        # Send 0 only if all inputs are high (NAND)
        output_val = PulseVal.LOW
        for input_value in self._input_values:
            if input_value == PulseVal.LOW:
                output_val = PulseVal.HIGH
                break

        return_pulses = []
        for output in self._outputs:
            return_pulses.append(Pulse(self, output, output_val))
        return return_pulses        

class Circuit():
    input_regex = re.compile(r"([%|&]?)(\w+)\s+->\s(.+)")
    def __init__(self, filename: str) -> None:
        self._flip_flops: [FlipFlop] = []
        self._conjunctions: [Conjunction] = []
        self._broadcaster: Broadcaster = None
        self._rx: PulseNode = None

        input_lines = open(filename).read().splitlines()
        # Track connections to make once all of the nodes are loaded
        connections = []
        node_name_hash = {}

        for line in input_lines:
            parts = self.input_regex.match(line).group
            new_node = None
            
            if parts(2) == "broadcaster":
                new_node = Broadcaster()
                self._broadcaster = new_node
            elif parts(1) == "%":
                new_node = FlipFlop()
                self._flip_flops.append(new_node)
            elif parts(1) == "&":
                new_node = Conjunction()
                self._conjunctions.append(new_node)
            else:
                new_node = PulseNode()

            node_name_hash[parts(2)] = new_node

            outputs = parts(3).split(", ")
            for output in outputs:
                connections.append((parts(2), output))                
        for connection in connections:
            sender = node_name_hash[connection[0]]
            # Load the receiver if known, otherwise just make
            # a basic element
            if (hash_receiver := node_name_hash.get(connection[1], None)) is not None:
                receiver = hash_receiver
            else:
                receiver = PulseNode()
                if connection[1] == "rx":
                    self._rx = receiver

            
            sender.connect_output(receiver)
            receiver.connect_input(sender)

    def is_in_initial_state(self) -> bool:
        for f in self._flip_flops:
            if f._stored_value:
                return False
        for c in self._conjunctions:
            for v in c._input_values:
                if v == PulseVal.HIGH:
                    return False
        return True

    def press_button(self) -> (int, int):
        pulse_queue = Queue()
        button_pulse = Pulse(None, self._broadcaster, PulseVal.LOW)
        pulse_queue.put(button_pulse)
        low_count = 0
        high_count = 0
        while not pulse_queue.empty():
            next_pulse: Pulse = pulse_queue.get()
            if next_pulse.value == PulseVal.LOW:
                low_count += 1
            else:
                high_count += 1
            new_pulses = next_pulse.receiver.handle_pulse(next_pulse.sender, next_pulse.value)
            for new_pulse in new_pulses:
                pulse_queue.put(new_pulse)
        return (low_count, high_count)

    def score(self, num_presses: int) -> int:
        low_count, high_count = self.press_button()
        i = 1
        running_totals = [(low_count, high_count)]
        while i < num_presses and not self.is_in_initial_state():
            new_low, new_high = self.press_button()
            low_count += new_low
            high_count += new_high
            running_totals.append((low_count, high_count))
            i += 1
        # If the circuit returned to its initial state before
        # the total number of button presses, calculate
        # what the total would be.
        if i < num_presses:
            print("Repeats after %d presses" % i)
            multiples = num_presses//i
            mod = num_presses % i

            low_total = multiples * running_totals[-1][0]
            high_total = multiples * running_totals[-1][1]            
            if mod > 0:
                low_total += running_totals[mod - 1]
                high_total += running_totals[mod - 1]
            return low_total * high_total

        return low_count * high_count
    
    def presses_for_rx(self) -> int:
        button_presses = 0
        pulse_queue = Queue()
        while True:
            button_pulse = Pulse(None, self._broadcaster, PulseVal.LOW)
            pulse_queue.put(button_pulse)
            button_presses += 1
            while not pulse_queue.empty():
                next_pulse: Pulse = pulse_queue.get()
                if next_pulse.value == PulseVal.LOW:
                    if next_pulse.receiver == self._rx:
                        return button_presses
                    
                new_pulses = next_pulse.receiver.handle_pulse(next_pulse.sender, next_pulse.value)
                for new_pulse in new_pulses:
                    pulse_queue.put(new_pulse)
            if self.is_in_initial_state():
                return -1

c = Circuit("data.txt")
print("Presses to activate RX: %d" % c.presses_for_rx())