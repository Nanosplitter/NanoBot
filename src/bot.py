
from tools import  *
from objects import *
from routines import *


# This file is for strategy

class ExampleBot(GoslingAgent):
    def run(agent):
        my_goal_to_ball, my_ball_distance = (agent.ball.location - agent.friend_goal.location).normalize(True)
        goal_to_me = agent.me.location - agent.friend_goal.location
        my_distance = my_goal_to_ball.dot(goal_to_me)

        foe_goal_to_ball, foe_ball_distance = (agent.ball.location - agent.foe_goal.location).normalize(True)
        if len(agent.foes) != 0:
            foe_goal_to_foe = agent.foes[0].location - agent.foe_goal.location
            foe_distance = foe_goal_to_ball.dot(foe_goal_to_foe)

        me_onside = my_distance - 200 < my_ball_distance
        if len(agent.foes) != 0:
            foe_onside = foe_distance - 200 < foe_ball_distance
        close = (agent.me.location - agent.ball.location).magnitude() < 2000
        have_boost = agent.me.boost > 20

        return_to_goal = False
        heading_to_goal = False
        if len(agent.stack) > 0:
            heading_to_goal = agent.stack[0].__class__.__name__ == "goto"
        
        left_field = Vector3(4200 * -side(agent.team), agent.ball.location.y + (1000 * -side(agent.team)), 0)
        right_field = Vector3(4200 * side(agent.team), agent.ball.location.y + (1000 * -side(agent.team)), 0)
        #targets = {"goal": ( agent.foe_goal.left_post + Vector3(side(agent.team) * 96, 0, 0), agent.foe_goal.right_post - Vector3(side(agent.team) * 96, 0, 0)), "upfield": (left_field, right_field)}
        targets = {"goal": ( agent.foe_goal.left_post, agent.foe_goal.right_post), "upfield": (left_field, right_field)}
    
        shots = find_hits(agent, targets)
        goals = [shot for shot in shots["goal"]]
        goals = sorted(goals, key=lambda shot: shot.intercept_time - agent.time)

        upfield = [shot for shot in shots["upfield"]]
        upfield = sorted(goals, key=lambda shot: shot.intercept_time - agent.time)

        can_shoot = False

        if len(upfield) + len(goals) > 0:
            can_shoot = True

        
        agent.debug(agent)
        
        
        me_onside=True

        if len(agent.stack) < 2:
            if agent.kickoff_flag:
                if len(agent.stack) < 1:
                    agent.push(kickoff())

            elif me_onside:
                if len(goals) > 0:
                        agent.push(goals[0])
                    #print("Shooting for goal")
                elif len(upfield) > 0 and abs(agent.friend_goal.location.y - agent.ball.location.y) < 8490:
                        agent.push(upfield[0])
                    #print("Upfield hit")

        
        
        if len(agent.stack) == 0:
            agent.push(goto(agent.friend_goal.location, vector=agent.ball.location))
            #agent.push(short_shot(agent.foe_goal.location))
        


    def goalInDanger(self):
        if self.team == 1:
            goal_y = self.friend_goal.location.y + 92.75
        else:
            goal_y = self.friend_goal.location.y - 92.75

        for s in self.ball_prediction_struct.slices:
            loc = s.physics.location
            if self.team == 1:
                if loc.y > goal_y:
                    return True
            else:
                if loc.y < goal_y:
                    return True
        return False
    
    def debug(self, agent, verbose=True):
        if verbose:
            agent.debug_stack()
            agent.line(agent.me.location, agent.foe_goal.left_post + Vector3(side(agent.team) * 200, 0, 0), [255, 255, 255])
            agent.line(agent.me.location, agent.foe_goal.right_post - Vector3(side(agent.team) * 200, 0, 0), [255, 255, 255])
