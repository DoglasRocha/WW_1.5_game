import pygame

class ImageLoader:
    
    directions = ['NORTH','SOUTH','EAST','WEST',
                  'NORTH WEST', 'NORTH EAST',
                  'SOUTH WEST', 'SOUTH EAST']
    
    @staticmethod
    def load_images(movable_type: str) -> dict:
        '''Method that load all the images of the thing specified.
        
        Receives the name of the movable in lowercase.'''
        images = {}
        
        for i in range(8):
            # saving the name to attribute in the dict
            direction = ImageLoader.directions[i]
            
            # defining the name of the file
            name = f'files/img/{movable_type}/{direction}.png'
            
            img = pygame.image.load(name) # loading the image
            images[direction] = img # putting the image in the dictionary
                
        return images
    
                    
             
            