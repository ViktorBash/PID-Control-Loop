# Thrust Vector Controlled Rocket Flight Code
This is a PID control loop made in Python and simulated in MATLAB intended to allow for thrust vector control of a model rocket.

### Workflow:
The PID controller is in PID.py. The test for the PID is in test_pid.py. Master.py will call PID and interact with it in order to connect Raspberry Pi 0W and IMU to the PID controller. 
Master.py will also determine current rocket state and carry out associated actions such as parachute deployment.  
Data.py will record data continuously through flight for post-launch review.
#
Contributors: Viktor Basharkevich and Robert Kirk
