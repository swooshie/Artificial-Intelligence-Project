(define (domain openrouter-routing)
  (:requirements :strips :typing)
  
  (:types 
    llm 
    provider 
    capability 
    request 
    account
    slot           ; discrete unit representing LLM capacity
    budgetunit     ; discrete unit representing account budget
  )
  
  (:predicates 
    (llm-available ?l - llm)
    (belongs-to ?l - llm ?p - provider)
    (has-capability ?l - llm ?c - capability)
    (request-assigned ?req - request)
    (assigned-to ?req - request ?l - llm)
    (requires-capability ?r - request ?c - capability)
    (belongs-to-account ?req - request ?a - account)
    ;; Resources predicates:
    (llm-has-slot ?l - llm ?s - slot)
    (account-has-promptunit ?a - account ?b - budgetunit)
    (account-has-completionunit ?a - account ?b - budgetunit)
  )
  
  (:action assign-request
    :parameters (?req - request ?cap - capability ?l - llm ?a - account ?s - slot ?p - budgetunit ?c - budgetunit)
    :precondition (and
      (llm-available ?l)
      (not (request-assigned ?req))
      (has-capability ?l ?cap)
      (requires-capability ?req ?cap)
      (belongs-to-account ?req ?a)
      (llm-has-slot ?l ?s)
      (account-has-promptunit ?a ?p)
      (account-has-completionunit ?a ?c)
    )
    :effect (and
      (assigned-to ?req ?l)
      (request-assigned ?req)
      (not (llm-has-slot ?l ?s))
      (not (account-has-promptunit ?a ?p))
      (not (account-has-completionunit ?a ?c))
    )
  )
)
