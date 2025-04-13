from enum import Enum

class QueueStrategy(Enum):
    FIFO = "fifo"
    LIFO = "lifo"
    PRIORITY = "priority"
    ROUND_ROBIN = "round_robin"