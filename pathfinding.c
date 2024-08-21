#include <stdio.h>
#include <stdbool.h>
#include <assert.h>
#include <string.h>
#define SIZE 10
#define LEFT 1
#define RIGHT 2
#define UP 3
#define DOWN 4
#define GOALNO 2

int main() {
    struct Square{
        struct Square* up;
        struct Square* down;
        struct Square* turnleft;
        struct Square* turnright;
        struct Square* backleft;
        struct Square* backright;
        struct Square* parent;
        int visited;
        bool state;
        int answer;
    } grid [SIZE+4][SIZE+4]; //x,y
    
    for(int i=0;i<SIZE+4;i++)for(int j=0;j<SIZE+4;j++){
        memset(grid[i]+j, 0, sizeof(struct Square));
    }

    bool issafe(int xtl, int ytl, int xbr, int ybr){
        //tl = top left, br = bottom right
        bool returnbool = false;
        for(int i=xtl;i<=xbr;i++)for(int j=ytl;j<=ybr;j++)
            returnbool += grid[i][j].state;
        return returnbool;
    } 
    
    // initialise border
    for(int i=0;i<SIZE;i++){
        int target[4] = {0,1,SIZE+2,SIZE+3};
        for(int j=0;j<SIZE;j++){
            grid[i][target[j]].state=true;
            grid[target[j]][i].state=true;
        }
    }
    
    //initialise obstacles and goals
    grid[5][7].answer = DOWN;
    grid[2][5].answer = LEFT;
    
    // define the paths here
    for(int x=2;x<SIZE;x++) for(int y=2;y<SIZE;y++){
        grid[x][y].up = issafe(x,y+1,x+1,y+1)?NULL:&grid[x][y+1];
        // Account for the back of the car being 1 square from camera
        grid[x][y].down = issafe(x,y-2,x+1,y-2)?NULL:&grid[x][y-1];
        // Assume camera on left
        grid[x][y].turnleft = issafe(x-2,y+2,x+1,y+1)?NULL:&grid[x-2][y+1];
        grid[x][y].turnright = issafe(x,y+2,x+3,y+1)?NULL:&grid[x+3][y+1];
    }
    
    printf("ORDER OF GOALS: ");
    int startx = 2, starty = 3;
    // Create a queue for BFS
    struct Square *queue[(SIZE+4)*(SIZE+4)];
    int front = 0, rear = 0;
    int goal = 0;

    // Mark the current node as visited and enqueue it
    grid[2][2].visited=1;
    queue[rear++] = grid[2]+2;
    struct Square *curr;
    // Iterate over the queue
    while (front != rear) {
      
        // Dequeue a vertex from queue and print it
        curr = queue[front++];
        if(curr->answer){
            printf("%d, ", curr->answer);
            if(++goal==GOALNO) break;
        } 
        
        // Get all adjacent vertices of the dequeued vertex
        // curr If an adjacent has not been visited,
        // then mark it visited and enqueue it
        if(curr->up && !curr->up->visited){
            curr->up->visited = UP;
            curr->up->parent = curr;
            queue[rear++] = curr->up;
        }
        if(curr->down && !curr->down->visited){
            curr->down->visited = DOWN;
            curr->down->parent = curr;
            queue[rear++] = curr->down;
        }
        if(curr->turnleft && !curr->turnleft->visited){
            curr->turnleft->visited = LEFT;
            curr->turnleft->parent = curr;
            queue[rear++] = curr->turnleft;
        }
        if(curr->turnright && !curr->turnright->visited){
            curr->turnright->visited = RIGHT;
            curr->turnright->parent = curr;
            queue[rear++] = curr->turnright;
        }
    }
    
    while(curr->parent){
        printf("%d,", curr->visited);
        curr=curr->parent;
    }

    return 0;
}