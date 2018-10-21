;; problem file: blocksworld-prob1.pddl

(define (problem prob) 
  (:domain blocksworld)
  (:objects a b)
  (:init (on-table a) (on-table b) (clear a) (clear b))
  (:goal (and (on a b))))
