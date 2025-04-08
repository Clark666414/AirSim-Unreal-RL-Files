import airsim
import time

client = airsim.MultirotorClient()                  # connect to the AirSim simulator
client.enableApiControl(True)                       # 获得控制权
client.armDisarm(True)                              # 解锁
client.takeoffAsync().join()                        # 第一阶段 ： 起飞

client.moveToZAsync(-3, 1).join()           # 第二阶段 ： 上升到两米

# 飞正方形
client.moveByVelocityZAsync(1, 0, -2,8).join()     # 第三阶段 ： 以1m/s速度向前飞8秒钟
client.moveByVelocityZAsync(0, 1, -2,8).join()     # 第三阶段 ： 以1m/s速度向右飞8秒钟
client.moveByVelocityZAsync(-1, 0, -2,8).join()     # 第三阶段 ： 以1m/s速度向后飞8秒钟
client.moveByVelocityZAsync(0, -1, -2,8).join()     # 第三阶段 ： 以1m/s速度向左飞8秒钟

# 悬停 2 秒钟
client.hoverAsync().join()                          #悬停两秒钟
time.sleep(2)

client.landAsync().jion()                           # 第五阶段 ： 降落
client.armDisarm(False)                             # 上锁
client.enableApiControl(False)                      # 释放控制权