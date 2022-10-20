from array import array
import numpy as np

axis_x = [1,0,0]
axis_y = [0,1,0]
axis_z = [0,0,1]


class Camera:
    def __init__(self):
        #  相机位置 
        self.position = [0, 0, 3]
        #  用来计算相机朝向 
        self.look_at = [0, 0, 0]
        #  相机向上的轴（计算相机旋转） 
        self.up = axis_y
        #  视角 
        self.fov = 45
        #  近平面位置 
        self.near = 1
        #  远平面 
        self.far = 1000
        #  视图比例 
        self.aspect = 1
        #  宽高（视图） 
        self.height = 1
        self.width = 1
    
    def set(self, position, look_at, up, fov, near,far):
        if (np.array_equal(position, look_at)):
            print ("failed: position is equal to look_at")
            return

        if (fov <= 0 or fov >= 180):
            self.fov = (fov + 180 ) % 180
        else:
            self.fov = fov

        self.position = position
        self.look_at = look_at
        self.up = up
        self.near = near
        self.far = far


    #  "世界->相机空间矩阵
    def world_to_camera_matrix(self):
        # 此处应为eye - target 如果使用target - eye，则坐标系从右手坐标系转换到了左手坐标系，会导致图像镜像
        # 见文档 https://blog.csdn.net/weixin_44179561/article/details/124149297
        n = self.norm(np.subtract(self.position,self.look_at))
        up = self.norm(self.up)
        #  up与朝向在同一轴上,点积为 +-1,选取x轴作为相机up 
        if(np.abs(np.dot(n,up) == 1)):
            self.up = [np.dot(n,up),0,0]
            if(np.abs(np.dot(n,up) == 1)):
                self.up = [0,0,np.dot(n,up)]
        
        v = self.norm(np.cross(n,up))
        u = self.norm(np.cross(v,n))
        # 旋转矩阵的齐次矩阵 推导见上链接 
        # 原理是 空间内一点可以同时使用世界坐标系的三周作为一个基去表示，也可以使用相机的三轴作为基表示，
        # 此时两组不同的解就对应两个坐标系内的坐标，因此相机的三轴可以直接写成一个矩阵表示 相机->世界 的旋转， 
        # 由于旋转矩阵是正交矩阵 此处世界->相机即可使用其转置矩阵作为逆矩阵
        rot = np.array([

            [u[0],u[1],u[2],0],
            [v[0],v[1],v[2],0],
            [n[0],n[1],n[2],0],
            [0,0,0,1]
        ])
        print(rot)
        # 位移矩阵就是将相机坐标系平移至原点与世界坐标系重合
        tran = np.array([
            [1,0,0,-self.position[0]],
            [0,1,0,-self.position[1]],
            [0,0,1,-self.position[2]],
            [0,0,0,1],
        ])
        # 先旋转再位移
        return np.matmul(rot,tran)

    #  透视视图矩阵 
    def perspective_matrix(self):
        return np.matmul(self.M_perspective(),self.world_to_camera_matrix())

    # 正交视图矩阵 
    def orthographic_matrix(self):
        return np.matmul(self.M_orthographic(),self.world_to_camera_matrix())

    # 正交投影矩阵
    def M_orthographic(self):
        halfSize = [self.width,self.height]
        return self.setOrthographic(-halfSize[0],halfSize[0],-halfSize[1],halfSize[1],self.near,self.far)

    # 透视投影矩阵 https://zhuanlan.zhihu.com/p/359128442
    def M_perspective(self):
        halfSize = self.getPerspectiveHalfSize()
        return self.setFrustum(-halfSize[0],halfSize[0],-halfSize[1],halfSize[1],self.near,self.far)
    
    def getPerspectiveHalfSize(self):
        width = self.near * np.tan(self.fov * np.pi / 360) *2
        height = width / self.aspect
        return [width,height]

    def norm(self,v):
        norm = np.linalg.norm(v)
        if norm == 0: 
            return v
        return v / norm

    # 透视投影矩阵，原理是根据z和far near将z对应的平面等比缩放 此处抄的playcanvas中的矩阵
    def setFrustum(self,left, right, bottom, top, znear, zfar):
        temp1 = 2 * znear
        temp2 = right - left
        temp3 = top - bottom
        temp4 = zfar - znear

        return np.array([
            [temp1 / temp2, 0,              (right + left) / temp2,     0],
            [0,             temp1 / temp3,  (top + bottom) / temp3,     0],
            [0,             0,              (-zfar - znear) / temp4,    (-temp1 * zfar) / temp4],
            [0,             0,              -1,                         0],
        ])
    
    # 正交投影矩阵 此处抄的playcanvas中的矩阵 推导过程见文档
    def setOrthographic(self,left, right, bottom, top, near, far):
        return np.array([
            [2 / (right - left),    0,                      0,                      -(right + left) / (right - left)],
            [0,                     2 / (top - bottom),     0,                      -(top + bottom) / (top - bottom)],
            [0,                     0,                      -2 / (far - near),      -(far + near) / (far - near)],
            [0,                     0,                      0,                      1],
        ])