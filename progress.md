# Progress

This document is for keeping track of progress and what is next. I guess I will use this instead of logseq, or maybe I can set up logseq to use this file? Would that mean that this file should be untracked?

## Idea

The idea of the project is sort of a social media type of platform based on making lists of things you like and ranking them.

So what is necessary:

- User model
- Treasure model
- Comment model

## Planning/To-Do's

- Translation? Django has a tool for this, and so does react, I guess I would need to do both.

## Branches

I want to document the point/goal of each branch here. This way, I can keep track of progress and what I plan to do next. It will also make documentation easier.

### Main

Things will be merged into this branch after tests pass.

### Backend

#### API Branch

I need to work on creating endpoints for each resource. I should create rough views, serializers, and models. Hook up the views to the relevant urls. Not sure what else should go in this branch. I think this branch should stick around and I can merge with main and then break off again to develop more of the API when I want.

I don't think I need to worry about filtering. Permissions can be put in later. Let me create some model view sets first and then maybe trim them down or specialize.

##### Users

What is the deal with my user class and the manager I have? what is the motiviation for having it? I think it is to have the username login credential be the email address.

Wrote initial tests for user model.

### Frontend
