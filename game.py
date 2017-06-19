import pygame
from pygame.locals import *
import sys

class Tower:
    def __init__(self,data = []):
        self.data = data

    def push(self,num):
        tmp = [num]
        tmp.extend(self.data)
        self.data = tmp

    def pop(self):
        return self.data.pop(0)

    def get_top(self):
        return self.data[0] if len(self.data)>0 else 0

    def print_tower(self):
        data = reversed(self.data)
        data = map(str,data)
        tower_str = "|" + "-".join(data)
        return tower_str
  
class HanoiTower:
    def __init__(self,size = 3):
        self.size = size
        self.towers = [Tower() for _ in xrange(3)]
        self.towers[0] = Tower(range(1,self.size+1))
        self.assist_queue = []
        self._is_solve = False

    def reset(self):
        self.towers = [Tower() for _ in xrange(3)]
        self.towers[0] = Tower(range(1,self.size+1))
        self._is_solve = False

    def calc_evaidx(self,src,dst):
        src_bit = (2-src)<<1
        dst_bit = (2-dst)<<1
        mask_bit = 0b111
        eva_bit = mask_bit ^ (src_bit | dst_bit)
        eva = 2
        while(eva_bit > 1):
            eva -=1
            eva_bit /=2
        return eva

    def is_solve(self):
        for i in xrange(self.size,0,-1):
            if self.get_locate_num(i)[0] != 2:
                return False
        return True

    def get_tower(self,i):
        return self.towers[i].data
    
    def get_locate_num(self,num):
        for i in xrange(3):
            if self.get_tower(i).count(num) <1:
                continue
            idx = self.get_tower(i).index(num)
            return (i,idx)
   
    def solve(self):
        self.instructs = []
        #self.print_towers()
        self.sol(0,2,self.size)
        
    def sol(self,src,dst,size):
        if size == 1:
            num = self.towers[src].pop()
            self.towers[dst].push(num)
            self.instructs.append((src,dst))
            #self.print_towers()
        else:
            """src_bit = (2-src)<<1
            dst_bit = (2-dst)<<1
            mask_bit = 0b111
            eva_bit = mask_bit ^ (src_bit | dst_bit)
            eva = 2
            while(eva_bit > 1):
                eva -=1
                eva_bit /=2"""
            eva = self.calc_evaidx(src,dst) 
            self.sol(src,eva,size-1)
            num = self.towers[src].pop()
            self.towers[dst].push(num)
            self.instructs.append((src,dst))
            #self.print_towers()
            self.sol(eva,dst,size-1)

    def move(self,src,dst):
        s = self.towers[src].get_top()
        d = self.towers[dst].get_top()
        if (s!=0) and (d == 0 or s<d) :
            self.towers[src].pop()
            self.towers[dst].push(s)

    def auto_move(self):
        if(len(self.instructs)>0):
            inst = self.instructs.pop(0)
            self.move(inst[0],inst[1])
            return True
        else:
            return False
    def assist(self):
        size = self.size
        self.assist_inst = []
        for i in xrange(size,0,-1):
            src,idx = self.get_locate_num(i)
            if src == 2:
                continue
            print "assist num{0} idx{1} src{2} dst2".format(i,idx,src)
            if self.atm_move(idx,src,2):
                break
        #print self.assist_inst
        if len(self.assist_inst) >0:
            inst = self.assist_inst.pop(len(self.assist_inst)-1)
            self.move(inst[0],inst[1])
            
    def atm_move(self,idx,src,dst):
        s_num = self.get_tower(src)[idx]
        dst_len = len(self.get_tower(dst))
        print "atm num{3} idx{0} src{1} dst{2}".format(idx,src,dst,s_num)
        if idx <0 or (src == dst):
            return False
        if idx == 0:   
            if dst_len < 1 or self.get_tower(dst)[0] > s_num:
                self.assist_inst.append((src,dst))
                return True
        eva = self.calc_evaidx(src,dst)
        d_num = self.towers[dst].get_top()
        d_idx = 0
        for d_idx in xrange(dst_len):    
            d_num = self.get_tower(dst)[d_idx]
            if d_num > s_num:
                d_idx -= 1
                d_num = self.get_tower(dst)[d_idx]
                break
        if idx != 0:
            up_num = self.get_tower(src)[idx-1]
            if d_num > s_num or up_num > d_num:
                return self.atm_move(idx-1,src,eva)
        return self.atm_move(d_idx,dst,eva)
                

        """    eva = self.calc_evaidx(src,dst)
            return self.atm_move(d_idx,dst,eva)
        
        eva = self.calc_evaidx(src,dst)
        return self.atm_move(idx-1,src,eva)"""
                      
    def print_towers(self):
        for i in xrange(3):
            print self.towers[i].print_tower()
        print ""

def paint_towers(screen,hanoi):
    #screen.fill((0, 0, 0, 0))
    lgth = width - (offsetx * 2)
    div = lgth /2

    for i in xrange(3):
        pygame.draw.line(screen, (100,100,100), (offsetx+div*i,5*offsety), (offsetx+div*i,length-offsety), 3)
        x = offsetx+div*i
        y = length - offsety
        l = (length - offsety)/hanoi.size
        l = 50 if l>50 else l
        w_rate = div / hanoi.size
        data = reversed(hanoi.towers[i].data)
        #print data
        for d in data:
            cols = [0,0,0]
            cols[d%3] = 1
            pygame.draw.rect(screen,(100+((cols[0])*20)%125,100+(cols[1]*20)%125,100+(cols[2]*20)%125),Rect(x-(d*w_rate/2),y-l,d*w_rate,l))
            y -=l-5

def paint_cursor(screen,cursor):
    #screen.fill((0, 0, 0, 0))
    lgth = width - (offsetx * 2)
    div = lgth /2 
    pygame.draw.circle(screen, (255,0,0), (offsetx+cursor*div,10), 10)

def main():
    pygame.init()
    screen = pygame.display.set_mode((width,length))
    args = sys.argv
    size = 3
    if len(args)>1:
        size = int(args[1])
    hanoi = HanoiTower(size)
    cursor = 0
    auto_flag = False
    while(True):
        paint_towers(screen,hanoi)
        paint_cursor(screen,cursor)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_1:
                    hanoi.move(cursor,0)
                if event.key == K_2:
                    hanoi.move(cursor,1)
                if event.key == K_3:
                    hanoi.move(cursor,2)
                if event.key == K_LEFT:
                    cursor = (cursor -1)%3
                if event.key == K_RIGHT:
                    cursor = (cursor +1)%3
                if event.key == K_r:
                    hanoi.reset()
                if event.key == K_h:
                    hanoi.assist()
                """if event.key == K_s:
                    hanoi.reset()
                    hanoi.solve()
                    hanoi.reset()"""
                if event.key == K_a:
                    hanoi.reset()
                    hanoi.solve()
                    hanoi.reset()
                    auto_flag = True
                    #hanoi.auto_move()
        if auto_flag:
            auto_flag = hanoi.auto_move()
        #screen.fill((0,0,0,0),Rect(0,0,width,length))
        if not hanoi._is_solve:
            if hanoi.is_solve():
                hanoi._is_solve = True
                print "Congratulation!!"
        pygame.display.update()
        pygame.time.wait(120)
        screen.fill((0,0,0))



width,length = 1080,480
offsetx = 200
offsety = 20

if __name__ == "__main__":
    main()
