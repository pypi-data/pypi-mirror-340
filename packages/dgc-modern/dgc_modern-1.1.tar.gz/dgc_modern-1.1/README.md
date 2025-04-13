DGC-Modern is Best Progres Bar Library!

## Installation

```bash
pip install dgc_modern
```

## Usage

```python
from dgc_modern import Task
```

### Progress Bar

```python
import time

t1 = Task(100, "Download A", process_color="green")
t2 = Task(50, "Processing B", process_color="yellow", iswaiting=True)

for i in range(100):
    t1.update()
    t2.update()
    time.sleep(0.05)

t2.waitmode(False)
for i in range(50):
    t2.update()
    time.sleep(0.1)

t1.finish()
t2.finish()
```
