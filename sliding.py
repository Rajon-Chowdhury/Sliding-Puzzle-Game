import pygame, sys, os, random




red = (200, 0, 0)
green = (0, 200, 0)
bright_red = (255,0,0)
bright_green = (0,255,0)
gameDisplay = pygame.display.set_mode((500, 600))

def text_objects(text,font):
    textSurface = font.render(text,True,(0,0,0))
    return textSurface, textSurface.get_rect()





class SlidePuzzle:
    def __init__(self,qs,ts,ms):
        self.qs,self.ts,self.ms = qs,ts,ms
        self.tiles_len = qs[0]*qs[1]-1
        self.tiles = [(x,y) for y in range(qs[1]) for x in range(qs[0])]
        self.tilepos = [(x*(ts+ms)+ms,y*(ts+ms)+ms) for y in range(qs[1]) for x in range(qs[0])]
        self.tilePOS = {(x,y):(x*(ts+ms)+ms,y*(ts+ms)+ms) for y in range(qs[1]) for x in range(qs[0])}
        self.fontt = pygame.font.Font('freesansbold.ttf',32)
        self.textX = 20
        self.textY = 550
        self.move = 0
        self.prev = None
        self.speed = 500

        self.rect = pygame.Rect(0,0,qs[0]*(ts+ms)+ms,qs[1]*(ts+ms)+ms)


        pic = pygame.transform.smoothscale(pygame.image.load('image.jpg'),self.rect.size)

        self.images = []; font = pygame.font.Font(None,120)
        for i in range(self.tiles_len):
            x,y = self.tilepos[i]
            image = pic.subsurface(x,y,ts,ts)
            text = font.render(str(i+1),2,(0,0,0)); w,h = text.get_size()
            image.blit(text,((ts-w)/2,(ts-h)/2)); self.images+=[image]





    def getBlank(self): return self.tiles[-1]
    def setBlank(self,pos): self.tiles[-1] = pos
    opentile = property(getBlank,setBlank)



    def switch(self,tile): self.tiles[self.tiles.index(tile)],self.opentile,self.prev = self.opentile,tile,self.opentile;self.move+=1;
    def in_grid(self,tile): return tile[0]>=0 and tile[0]<self.qs[0] and tile[1]>=0 and tile[1]<self.qs[1]
    def adjacent(self): x,y = self.opentile; return (x-1,y), (x+1,y),(x,y-1),(x,y+1)

    def random(self): adj = self.adjacent(); self.switch(random.choice([pos for pos in adj if self.in_grid(pos) and pos!=self.prev]))




    def update(self,dt,screen):

       s = self.speed*dt
       mouse = pygame.mouse.get_pressed()

       mpos = pygame.mouse.get_pos()
       if self.move<100:
          for i in range(100): self.random()

       if mouse[0]:
           x,y = mpos[0]%(self.ts+self.ms),mpos[1]%(self.ts+self.ms)
           if x>self.ms and y>self.ms:
              tile = mpos[0]//self.ts,mpos[1]//self.ts
              if self.in_grid(tile) and tile in self.adjacent(): self.switch(tile)
       for i in range(self.tiles_len):
            x,y = self.tilepos[i]
            X,Y = self.tilePOS[self.tiles[i]]
            dx,dy = X-x,Y-y
            x = (X if abs(dx)<s else x+s if dx>0 else x-s)
            y = (Y if abs(dy)<s else y+s if dy>0 else y-s)
            self.tilepos[i] = x,y


    def draw(self,screen,h):
       for i in range(self.tiles_len):
           x,y = self.tilepos[i]
           screen.blit(self.images[i],(x,y))
       if self.move>100:
          score = self.fontt.render("Moves : " + str(self.move-100), True, (255, 0, 255))
          screen.blit(score, (self.textX, h-70))

       button("Back",400,h-80,80,40,green,bright_green,"back")

    def events(self,event):
        if event.type == pygame.KEYDOWN:
            for key,dx,dy in (pygame.K_w,0,-1),(pygame.K_s,0,1),(pygame.K_a,-1,0),(pygame.k_d,1,0):
                if event.key == key:
                    x,y = self.opentile; tile = x+dx,y+dy
                    if self.in_grid(tile): self.switch(tile)

            if event.key == pygame.K_SPACE:
                for i in range(100): self.random()




def start_game(x,y,w,h):
        screen = pygame.display.set_mode((w, h))
        fpsclock = pygame.time.Clock()
        program = SlidePuzzle((x, y), 160, 5)

        while True:
            dt = fpsclock.tick() / 1000

            screen.fill((0, 0, 0))
            program.draw(screen,h)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                program.events(event)

            program.update(dt, screen)





def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] >y:
        pygame.draw.rect(gameDisplay,ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            if action =="lev1":
                start_game(3,3,500,600)
            elif action =="lev2":
               start_game(4,4,700,800)
            elif action =="back":
               game_intro()

    else:
        pygame.draw.rect(gameDisplay,ic,(x,y,w,h))

    smallText = pygame.font.Font("freesansbold.ttf",14)
    TextSurf, TextRect = text_objects(msg, smallText)
    TextRect.center = ((x+(w/2)),(y+(h/2)))
    gameDisplay.blit(TextSurf, TextRect)


def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()

        gameDisplay.fill((255,255,255))
        largeText = pygame.font.Font('freesansbold.ttf',50)
        TextSurf, TextRect = text_objects("Puzzle Game!!",largeText)
        TextRect.center = (250,300)
        gameDisplay.blit(TextSurf, TextRect)

        button("3 X 3",50,450,100,50,green,bright_green,"lev1")
        button("4 X 4",350,450,100,50,red,bright_red,"lev2")


        pygame.display.update()







def main():
    pygame.init()

    pygame.display.set_caption('Slide puzzle')

    game_intro()



if __name__ == '__main__':
    main()