#!/bin/bash
# Author: David Ackerson

# Save the start time
date > $2.time

# Run the provided script
nice ./$1 $2

# Save the end time
date >> $2.time
