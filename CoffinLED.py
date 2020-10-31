import board
import RPi.GPIO as GPIO
import neopixel
import _thread
import time
from pubsub import pub



RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
PINK = (255, 0, 174)
WHITE = (255,255,255)
BLACK = (0,0,0)


class CoffinLED():
    
    def __init__(self):
        self.wait = .5
        self.pixel_numbers = 300
        self.pixels = neopixel.NeoPixel(board.D18, self.pixel_numbers)
        self.pixels.fill((0, 0, 0))
        pub.subscribe(self.led_listener, 'LED-MESSAGES')

    def led_listener(self, color, msg=None):
        print('Function led_listener received color: %s ' % str(color))
        if msg == "colorWipe":
            self.colorWipe(color)
        elif msg == "strobe":
            self.strobe(RED)
        else:
            self.set_strip_color(color)


    def strobe(self, color, wait_ms=.2):
        for i in range(5):
            for i in range(self.pixel_numbers):
                self.pixels.fill(color)
                time.sleep(wait_ms)
                self.pixels.fill(BLACK)
                time.sleep(wait_ms)




    def colorWipe(self, color, wait_ms=5):
        """Wipe color across display a pixel at a time."""
        for i in range(self.pixel_numbers):
            self.pixels.setPixelColor(i, color)
            self.pixels.show()
            time.sleep(wait_ms / 1000.0)

    def get_random_color(self):
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)
        color = (r,g,b)
        return color

    def set_random_strip_color(self, delay):
         _thread.start_new_thread(self._set_random_strip_color(delay))

    def set_strip_color(self, color):
        self.pixels.fill(color)
        
    def _set_random_strip_color(self, delay):
            color = self.get_random_color()
            self.pixels.fill(color)
            sleep(delay)
            self.pixels.fill(BLACK)
            sleep(delay)
            return(color)

    def lightning(self,strike_count):
        print(strike_count)
        if strike_count == -1:
            strike_count = random.randint(0,4)
        print(strike_count)
        for x in range(strike_count):
            d1 = randint(0,len(lightning_delay))
            d2 = randint(0,len(lightning_delay))

            print("Striking %d " % strike_count)
            print("Lightning is striking!")
            self.pixels.fill((0, 0, 0))
            self.pixels.fill((255, 255, 255))
        
            sleep(d1)
            self.pixels.fill((255, 255, 255))
            sleep(d2)
            self.pixels.fill((0, 0, 0))
        self.pixels.fill((0, 0, 0))

    def fill_pixels(self, r, g, b):
        for i in range(0, self.pixel_numbers):
            self.pixels[i] = (r, g, b)
            self.pixels.write()
 
    
    # Get the color of a pixel within a smooth gradient of two colors.
    # Starting R,G,B color
    # Ending R,G,B color
    # Position along gradient, should be a value 0 to 1.0
    
    
    def color_gradient(self, start_r, start_g, start_b, end_r, end_g, end_b, pos):
        # Interpolate R,G,B values and return them as a color.
        red = lerp(pos, 0.0, 1.0, start_r, end_r)
        green = lerp(pos, 0.0, 1.0, start_g, end_g)
        blue = lerp(pos, 0.0, 1.0, start_b, end_b)
    
        return (red, green, blue)

    def animate_gradient_fill(self, start_r, start_g, start_b, end_r, end_g, end_b,
                          duration_ms):
        start = time.monotonic()
    
        # Display start color.
        self.fill_pixels(start_r, start_g, start_b)
    
        # Main animation loop.
        delta = time.monotonic() - start
    
        while delta < duration_ms:
            # Calculate how far along we are in the duration as a position 0...1.0
            pos = delta / duration_ms
            # Get the gradient color and fill all the pixels with it.
            color = self.color_gradient(start_r, start_g, start_b,
                                end_r, end_g, end_b, pos)
            self.fill_pixels(int(color[0]), int(color[1]), int(color[2]))
            # Update delta and repeat.
            delta = time.monotonic() - start
    
        # Display end color.
        self.fill_pixels(end_r, end_g, end_b)

if __name__ == "__main__":
    l = CoffinLED()
    while 1:
        l.set_strip_color((0,255,0))
