import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for item in self.domains:
            for word in item.words:
                if max(item.height, item.width) != len(word):
                    self.domains[item].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        overlap = self.overlaps(x,y)
        domains_y = list(self.domains[y])
        
        revised = False

        for domain_x in self.domains[x]:
            for domain_y in domains_y:
                if domain_x != domain_y and domain_x[overlap[0]] == domain_y[overlap[1]]: # constraint satisfied
                    break
                if domains_y.index(domain_y)+1 == len(domains_y): # if last item in list but still not constraint satisfactory
                    self.domains[x].remove(domain_x)
                    revised = True
        
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        
        # queue = all arcs in csp
        # while queue non-empty:
        #   (x,y) = dequeue(queue)
        #   if revise(x,y):
        #       if size of X.domain == 0:
        #           return false
        #       for each Z in X.neighbors-{y}:
        #            enqueue(queue, z,x)
        
        # Create intiial queue
        queue = set()
        for variable, domains in self.domains:
            for neighbor in self.neighbors(variable):
                queue.add(sorted((variable, neighbor)))
        
        while queue:
            x, y = queue.pop()
        
        if revise(x,y):
            if len(self.domains[x]) == 0:
                return False
            for z in self.neighbors(x)
                if z == y: break
                queue.add(sorted((x,z)))
        return True
            
        
        
    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if len(assignment) = len(self.domains):
            return True
        
        # maybe I should check if every value in key-value pair is not None
        return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        
        assigned_words = []
        
        for variable in assignment:
            words = assignment[variable]
            
            for word in words:
                assigned_words.append(word)
                if len(word) != max(self.domains[variable].height, self.domains[variable].width):
                    return False
                
                for neighbor in self.neighbors(variable):
                    overlap_variable, overlap_neighbor = self.overlaps(variable, neighbor)
                    if variable[overlap_variable] != neighbor[overlap_neighbor]:
                        return False
            
        if len(words) != len(set(words)):
            return False
        
        return True
        
    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        order_domain_values = {}
        
        words = self.domains[variable][1]
        neighbors = self.neighbors(var)
        
        for word in words:
            conflicts = 0
            
            for neighbor in neighbors:
                
                if neighbor in assignment:
                    continue
                
                overlaps = self.crossword.overlaps[var, neighbor]
                possible_conflicts = self.domains[neighbor][1]
                
                for possible_conflict in possible_conflicts:
                    if word == possible_conflict:
                        conflicts += 1
                        break
                    if word[overlaps[0]] != neighbor[overlaps[1]]:
                        conflicts += 1
                        break
            
            order_domain_values[word] = conflicts
        
        order_domain_values = dict(sorted(order_domain_values.items(), key=lambda item: item[1]))
        order_domain_values = list(order_domain_values)
        
        return order_domain_values
        

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        for domain in self.order_domain_values():
            if domain not in assignment:
                return domain
            

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.domains:
            assignment[var] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result != failure:
                    return result
                del assignment[var]
            else:
                del assignment[var]
        return failure
            


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
