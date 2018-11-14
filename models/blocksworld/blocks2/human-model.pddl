(define (domain BLOCKS)
  (:requirements :strips)
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

(not ( on ?x ?y ))
(not ( clear ?x ))
(not ( handempty ))
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
( holding ?x )
(not ( clear ?x ))
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
( on ?x ?y )
(not ( holding ?x ))
)
)


)
