import pygame

class ImageLoader:
    
    directions = ['NORTH','SOUTH','EAST','WEST',
                  'NORTH WEST', 'NORTH EAST',
                  'SOUTH WEST', 'SOUTH EAST']
    
    @staticmethod
    def load_character() -> dict:
        '''Method that load all the images of the character.'''
        images = {}
        
        for i in range(8):
            # saving the name to attribute in the dict
            direction = ImageLoader.directions[i]
            
            # defining the name of the file
            name = f'files/img/character/{direction}.png'
            
            try:
                img = pygame.image.load(name) # loading the image
                images[direction] = img # putting the image in the dictionary
                breakpoint()
            except FileNotFoundError:
                return images
            breakpoint()
        
        return images
                    
             
            