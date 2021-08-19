import pygame

class ImageLoader:
    
    
    @staticmethod
    def load_images(movable_type: str) -> dict:
        '''Method that load all the images of the thing specified.
        
        Receives the name of the movable in lowercase.'''
        # all possible directions
        directions = ('NORTH','SOUTH','EAST','WEST',
                  'NORTH WEST', 'NORTH EAST',
                  'SOUTH WEST', 'SOUTH EAST')
        
        images = {}
        
        for direction in directions:
            # defining the name of the file
            name = f'files/img/{movable_type}/{direction}.png'
            
            img = pygame.image.load(name) # loading the image
            images[direction] = img # putting the image in the dictionary
                
        return images
    
    @staticmethod
    def load_scenary() -> dict:
        '''Method that loads all the little blocks that compose the scenary. 
        
        Returns a dict with the images loaded and ready to be blitted.'''
        
        # tuple that holds all the names of the little blocks of the scenary
        blocks = ('grass', 'path', 'scenary_limit', 'stone_path',
                  'high_fence', 'spawn_wall', 'heavy_mud',
                  'light_mud', 'barbwire', 'bad_wall', 'bullets',
                  ) 
        
        images = {}
        
        for block_name in blocks:
            name = f'files/img/scenary/{block_name}.png'
            
            img = pygame.image.load(name)
            images[block_name] = img

        return images 
                                        