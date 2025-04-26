(define (problem route-requests)
  (:domain openrouter-routing)
  (:objects
    ;; LLMs: Added four LLMs
    gpt4 claude3 bingchat bard - llm

    ;; Providers: One for each LLM
    openai anthropic microsoft google - provider

    ;; Capabilities: Expanded to include four different capabilities
    coding multilingual safe-for-kids long-context - capability

    ;; Five requests
    req1 req2 req3 req4 req5 - request

    ;; One account (for simplicity)
    acc1 - account

    ;; Capacity slots: total slots >= number of requests
    s1 s2 - slot           ; gpt4 has 2 slots
    s3 s4 - slot           ; claude3 has 2 slots
    s5 - slot              ; bingchat has 1 slot
    s6 - slot              ; bard has 1 slot

    ;; Account budget units: 5 prompt units and 5 completion units for 5 requests
    bp1 bp2 bp3 bp4 bp5 - budgetunit
    bc1 bc2 bc3 bc4 bc5 - budgetunit
  )
  
  (:init
    ;; LLM availability
    (llm-available gpt4)
    (llm-available claude3)
    (llm-available bingchat)
    (llm-available bard)
    
    ;; Provider mapping 
    (belongs-to gpt4 openai)
    (belongs-to claude3 anthropic)
    (belongs-to bingchat microsoft)
    (belongs-to bard google)
    
    ;; LLM capabilities:
    (has-capability gpt4 coding)
    (has-capability gpt4 multilingual)
    (has-capability gpt4 long-context)
    
    (has-capability claude3 multilingual)
    (has-capability claude3 safe-for-kids)
    
    (has-capability bingchat coding)
    (has-capability bingchat safe-for-kids)
    (has-capability bingchat multilingual)
    
    (has-capability bard multilingual)
    (has-capability bard long-context)
    
    ;; Request requirements: Each request requires one capability
    (requires-capability req1 coding)
    (requires-capability req2 multilingual)
    (requires-capability req3 long-context)
    (requires-capability req4 safe-for-kids)
    (requires-capability req5 multilingual)
    
    ;; Associate each request with the account:
    (belongs-to-account req1 acc1)
    (belongs-to-account req2 acc1)
    (belongs-to-account req3 acc1)
    (belongs-to-account req4 acc1)
    (belongs-to-account req5 acc1)
    
    ;; LLM capacity: Assign available slots to each LLM
    (llm-has-slot gpt4 s1)
    (llm-has-slot gpt4 s2)
    
    (llm-has-slot claude3 s3)
    (llm-has-slot claude3 s4)
    
    (llm-has-slot bingchat s5)
    
    (llm-has-slot bard s6)
    
    ;; Account budgets: 5 prompt units and 5 completion units
    (account-has-promptunit acc1 bp1)
    (account-has-promptunit acc1 bp2)
    (account-has-promptunit acc1 bp3)
    (account-has-promptunit acc1 bp4)
    (account-has-promptunit acc1 bp5)
    
    (account-has-completionunit acc1 bc1)
    (account-has-completionunit acc1 bc2)
    (account-has-completionunit acc1 bc3)
    (account-has-completionunit acc1 bc4)
    (account-has-completionunit acc1 bc5)
  )
  
  (:goal (and
    (request-assigned req1)
    (request-assigned req2)
    (request-assigned req3)
    (request-assigned req4)
    (request-assigned req5)
  ))
)
