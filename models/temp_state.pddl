
(define (domain blocksworld)
  (:requirements :strips)
(:predicates (clear ?x)
             (on-table ?x)
             (holding ?x)
             (on ?x ?y))

(:action pickup
  :parameters (?ob)
  :precondition (and (clear ?ob) )
  :effect (and (holding ?ob) (not (on-table ?ob)) (not (clear ?ob)) ))

(:action unstack
  :parameters (?ob ?underob)
  :precondition (and (clear ?ob) (on ?ob ?underob) )
  :effect (and (clear ?underob) (holding ?ob) (not (on ?ob ?underob)) (not (clear ?ob)) ))

(:action putdown
  :parameters (?ob)
  :precondition (and (holding ?ob) )
  :effect (and (on-table ?ob) (clear ?ob) (not (holding ?ob)) ))

(:action stack
  :parameters (?ob ?underob)
  :precondition (and (holding ?ob) (clear ?underob) )
  :effect (and (on ?ob ?underob) (clear ?ob) (not (holding ?ob)) (not (clear ?underob)) ))
)