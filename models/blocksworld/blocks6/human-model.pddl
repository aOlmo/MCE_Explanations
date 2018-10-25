(define (domain BLOCKS)
  (:requirements :strips)
  (:types block)
  (:predicates (on ?x ?y)
           (ontable ?x)
           (clear ?x)
           (handempty)
           (holding ?x)
           )

(:action unstack
:parameters (?x ?y)
:precondition
(and
( on ?x ?y )
( clear ?x )
( handempty )
)
:effect
(and
( holding ?x )
(not ( on ?x ?y ))
(not ( clear ?x ))
)
)

(:action pickup
:parameters (?x)
:precondition
(and
( clear ?x )
( ontable ?x )
( handempty )
)
:effect
(and

(not ( handempty ))
)
)

(:action putdown
:parameters (?x)
:precondition
(and

)
:effect
(and
( clear ?x )
( handempty )
(not ( holding ?x ))
)
)

(:action stack
:parameters (?x ?y)
:precondition
(and
( holding ?x )
( clear ?y )
)
:effect
(and

(not ( clear ?y ))
)
)


)
