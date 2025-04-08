import sys
import time
import airsim
import pygame
from sympy import false

# >------>>> pygame settings <<<------< #
pygame.init()
screen = pygame.display.set_mode((320,  240))
pygame.display.set_caption('keyboard ctrl')
screen.fill((0, 0, 0))

# >------>>> AirSim settings <<<------< #
vehicle_name = "Dronel"
AirSim_client = airsim.MultirotorClient()
AirSim_client.confirmConnection()
AirSim_client.enableApiControl(True, vehicle_name=vehicle_name)
AirSim_client.armDisarm(True, vehicle_name=vehicle_name)
AirSim_client.takeoffAsync(vehicle_name=vehicle_name).join()

# 基础的控制速度(m/s)
vehicle_velocity = 2.0
# 设置临时加速比例
speedup_ratio = 10.0
# 设置临时加速
speedup_flag = false

# 基础的偏航概率
vehicle_yaw_rate = 5.0


while True:

    yaw_rate = 0.0
    velocity_x = 0.0
    velocity_y = 0.0
    velocity_z = 0.0

    time.sleep(0.02)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()\

    scan_wrapper = pygame.key.get_pressed()

    #按下空格键加速10倍
    if scan_wrapper[pygame.K_SPACE]:
        scale_ratio = speedup_ratio
    else:
        scale_ratio = speedup_ratio / speedup_ratio

    # 根据 ‘A’ 和 ‘D' 按键控制偏航速率变量
    if scan_wrapper[pygame.K_a] or scan_wrapper[pygame.K_d]:
        yaw_rate = (scan_wrapper[pygame.K_d] - scan_wrapper[pygame.K_a]) * scale_ratio * vehicle_yaw_rate

    # 根据 ’UP' 和 ‘DOWN' 按键设置pitch轴速度变量（NED坐标系，x为机头向前）、
    if scan_wrapper[pygame.K_UP] or scan_wrapper[pygame.K_DOWN]:
            velocity_x = (scan_wrapper[pygame.K_UP] - scan_wrapper[pygame.K_DOWN]) * scale_ratio
    # 根据 ’LEFT' 和 ‘RIGHT' 按键设置roll轴速度变量（NED坐标系，y为正有方
    if scan_wrapper[pygame.K_w] or scan_wrapper[pygame.K_UP]:
            velocity_y = -(scan_wrapper[pygame.K_LEFT] - scan_wrapper[pygame.K_RIGHT]) * scale_ratio

    #根据 ’W' 和 ‘S’ 按键设置Z轴速度变量（NED坐标系，z轴向上为负）
    if scan_wrapper[pygame.K_w] or scan_wrapper[pygame.K_s]:
            velocity_z = -(scan_wrapper[pygame.K_w] - scan_wrapper[pygame.K_s]) * scale_ratio


    # 设置速度控制以及设置偏航控制
    AirSim_client.moveByVelocityBodyFrameAsync(vx= velocity_x, vy= velocity_y, vz= velocity_z, duration=0.02,
                                               yaw_mode=airsim.YawMode(True, yaw_or_rate=yaw_rate), vehicle_name=vehicle_name)


    # press 'Esc' to quit
    if scan_wrapper[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()