import json
from datetime import datetime

class ScoreManager:
    
    
    def __init__(self):
        self.general_score = 0.0
        self.level_score = 0.0
        self.attempt = 1
        self.all_scores = ScoreManager.__read_scores('five_biggest_scores.json')
        self.five_biggest_scores = self.five_biggest_scores_organizer()
        
    def add_points(self, points: int) -> float:
        real_points = points / self.attempt
        self.level_score += real_points
        
    def re_init_level(self) -> None:
        self.level_score = 0
        self.attempt += 1
        
    def to_next_level(self) -> None:
        self.general_score += self.level_score
        self.level_score = 0
    
    @staticmethod
    def __read_scores(file: str) -> dict:
        try:
            with open(file, 'r') as f:
                scores = json.load(f)
        except FileNotFoundError:
            with open(file, 'w') as f:
                json.dump({}, f)
                scores = {}
        
        return scores
    
    @staticmethod
    def __sort_in_crescent_order(scores: dict) -> list:
        sorted_scores = []
        
        for key, value in scores.items():
            if len(sorted_scores) <= 0 and value != 0:
                sorted_scores.append((key, value))
                    
            else:
                for score in sorted_scores:
                    _key = score[0]
                    _value = score[1]
                        
                    if (key, value) in sorted_scores:
                        break
                        
                    if value > _value:
                        sorted_scores.insert(sorted_scores.index(score), (key, value))
                            
                else:
                    sorted_scores.append((key, value))
                    
        return sorted_scores
    
    @staticmethod
    def __select_first_five_values(scores: list) -> dict:
        new_five_biggest_scores = {}
        
        if len(scores) < 5:
            for key, value in scores:
                new_five_biggest_scores[key] = value
        else:
            for i in range(5):
                score = scores[i]
                key = score[0]
                value = score[1]
                
                new_five_biggest_scores[key] = value
                
        return new_five_biggest_scores
    
    def five_biggest_scores_organizer(self) -> dict:
        '''Algorithm to put all the scores in crescent order and get the five bigger'''
        
        scores = ScoreManager.__sort_in_crescent_order(self.all_scores)
        five_biggest_scores = ScoreManager.__select_first_five_values(scores)
        
        return five_biggest_scores
        
    def save_score(self) -> None:
        if self.general_score != 0:
            date_now = datetime.now()
            formated_date = f'{date_now.day}/{date_now.month}/{date_now.year}, {date_now.hour}:{date_now.minute}'
            
            self.all_scores[formated_date] = self.general_score
            
            with open('five_biggest_scores.json', 'w') as f:
                json.dump(self.all_scores, f)
    
    def get_general_score(self) -> float:
        return self.general_score

    def get_level_score(self) -> float:
        return self.level_score
    
    def get_attempt(self) -> int:
        return self.attempt
    
    def get_five_biggest_scores(self) -> dict:
        return self.five_biggest_scores