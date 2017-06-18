# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from game import Directions

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    """
    Pseudocode: 
        Stack s; 
        for each vertex u, set visited[u] to false
        push start location onto Stack
        while (S is not empty): 
            pop off an element from the stack

            if element is goal: 
                return the list of actions taken to get this node


            if it has not been visited yet: 
                set that its been visited

                for each unvisited neighbor w of u (extend the fringe or frontier):
                    push w onto Stack
    """
    # Create a new stack s
    stack = util.Stack()
    # pqueue = util.PriorityQueue()

    # Create a list of visited nodes
    visited = []

    # Start position tuple
    start = (problem.getStartState(), Directions.STOP, 0)

    # Push the start state onto the stack
    stack.push([start])
    # pqueue.push([start], 0)

    # While the stack is not empty
    while not stack.isEmpty():
    # while not pqueue.isEmpty(): 

        # Pop off an element from the stack
        currentPlan = stack.pop()
        # currentPlan = pqueue.pop()

        # If element is goal
        currentState = currentPlan[len(currentPlan)-1][0]
        if problem.isGoalState(currentState): 
            directions = [ path[1] for path in currentPlan if path[1] != Directions.STOP ]
            return directions

        # If element has not been visited
        if currentState not in visited: 

            # Indicate that the element has been visited
            visited.append(currentState)

            # For each unvisited neighbor of u
            successors = problem.getSuccessors(currentState)
            for succ in successors: 
                # Push the neighbor onto the stack
                if succ[0] not in visited:
                    newPlan = [succ]
                    stack.push(currentPlan + newPlan)
                    # pqueue.push(currentPlan + newPlan, problem.getCostOfActions(currentPlan[1]))

    return None

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    """
    Pseudocode: 

    Queue queue;
    Goal test the start location
    Add the start location to the queue
    Initialize the visited list

    loop: 
        if the frontier is empty, return failure
        pop a node off the frontier
        add the node to the visited list
        for each of its successors: 
            if the child is not in the explored or frontier:
                if the child is the goal, return solution
                insert the child into the frontier
    """
    # Create a new queue 
    queue = util.Queue()

    # Create a list of visited nodes
    visited = []

    # Start position tuple
    start = (problem.getStartState(), Directions.STOP, 0)

    # Goal test the start
    if problem.isGoalState(start[0]): 
        return [start[1]]

    # Push the start state onto the queue
    queue.push([start])

    while not queue.isEmpty(): 

        # Pop off an element from the queue
        currentPlan = queue.pop()

        # Get the current state location from plan
        currentState = currentPlan[len(currentPlan)-1][0]

        # Add node to visited list
        visited.append(currentState)

        # Get the successors for current state
        successors = problem.getSuccessors(currentState)

        # For each successor 
        for succ in successors: 
            succState = succ[0]

            # TODO: How to check if succState is not in frontier ???
            if succState not in visited: 
                updatedPlan = currentPlan + [succ]
                if problem.isGoalState(succState): 
                    directions = [ path[1] for path in updatedPlan if path[1] != Directions.STOP ]
                    return directions
                queue.push(updatedPlan)

    return None

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    """
    Pseudocode: 

    PriorityQueue pqueue
    Add the start location to the priority queue
    Initialize list of visited nodes

    while frontier is not empty: 
        pop node off the frontier
        if node is goal, return solution
        add node to list of visited 
        for each successor of node: 
            if successor is not explored or in frontier: 
                insert child into frontier
            else if child is in frontier with higher path-cost,
                replace original frontier node with child
    """
    priorityQueue = util.PriorityQueue()

    visited = []

    start = (problem.getStartState(), Directions.STOP, 0)

    priorityQueue.push([start], problem.getCostOfActions([Directions.STOP]))

    while not priorityQueue.isEmpty(): 
        currentPlan = priorityQueue.pop()

        currentState = currentPlan[len(currentPlan)-1][0]
        if problem.isGoalState(currentState): 
            directions = [ path[1] for path in currentPlan if path[1] != Directions.STOP ]  
            return directions

        visited.append(currentState)

        successors = problem.getSuccessors(currentState)
        for succ in successors: 
            succState = succ[0]
            if succState not in visited: 
                updatedPlan = currentPlan + [succ]
                updatedPlanCost = problem.getCostOfActions([ path[1] for path in updatedPlan if path[1] != Directions.STOP ])
                priorityQueue.update(updatedPlan, updatedPlanCost)

    return None
def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    """
    f(n) = h(n) + g(n)
    f(n) = estimated cost of cheapest solution through n 
    h(n) = estimated cost of cheapest path from n to the goal
    g(n) = path cost from start node to node n
    """

    priorityQueue = util.PriorityQueue()

    visited = []

    start = (problem.getStartState(), Directions.STOP, 0)
    gStart = problem.getCostOfActions([start[1]])
    hStart = heuristic(start[0], problem)
    fStart = gStart + hStart 

    priorityQueue.push([start], fStart)

    while not priorityQueue.isEmpty(): 
        currentPlan = priorityQueue.pop()

        currentState = currentPlan[len(currentPlan)-1][0]
        if problem.isGoalState(currentState): 
            directions = [ path[1] for path in currentPlan if path[1] != Directions.STOP ]
            return directions

        visited.append(currentState)

        successors = problem.getSuccessors(currentState)
        for succ in successors: 
            succState = succ[0]
            if succState not in visited: 
                updatedPlan = currentPlan + [succ]
                updatedPlanPath = [ path[1] for path in updatedPlan if path[1] != Directions.STOP ]
                gUpdatedPlan = problem.getCostOfActions(updatedPlanPath)
                hUpdatedPlan = heuristic(succState, problem)
                fUpdatedPlan = gUpdatedPlan + hUpdatedPlan
                priorityQueue.update(updatedPlan, fUpdatedPlan)

    return None

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
