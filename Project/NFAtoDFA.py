from queue import Queue

q ,s ,a ,m ,n = map(int,input().split())

states_nfa = list(range(q))

Sigma = [input() for i in range(s)]

q0_nfa = int(input())

A_nfa = [int(input()) for i in range(a)]

transitions_nfa = []
for _ in range(m):
    qi, symbol, qj = input().split()
    qi = int(qi)
    qj = int(qj)
    transitions_nfa.append((qi, symbol, qj))

Test_Cases = [input() for i in range(n)]

def lambda_closure(states, transitions_nfa, q_initial):
    closure = set()
    queue = Queue()
    closure.add(q_initial)
    queue.put(q_initial)
    while not queue.empty():
        state = queue.get()
        for transition in transitions_nfa:
            qi, symbol, qj = transition
            if qi == state and symbol == '$' and qj not in closure:
                closure.add(qj)
                queue.put(qj)
    return closure

def move(states, transitions_nfa, symbols):
    moved_states = set()
    for state in states:
        for symbol in symbols:
            for transition in transitions_nfa:
                qi, transition_symbol, qj = transition
                if qi == state and transition_symbol == symbol:
                    moved_states.add(qj)
    return moved_states

def NFA_to_DFA_conversion(states_nfa, Sigma, q0_nfa, A_nfa, transitions_nfa):
    dfa_states = []
    dfa_accepting_states = []
    dfa_transitions = []

    initial_closure = lambda_closure({q0_nfa}, transitions_nfa, q0_nfa)
    dfa_states.append(initial_closure)
    if bool(initial_closure.intersection(A_nfa)):
        dfa_accepting_states.append(initial_closure)

    queue = Queue()
    queue.put(initial_closure)

    while not queue.empty():
        current_states = queue.get()
        for symbol in Sigma:
            moved_states = move(current_states, transitions_nfa, symbol)
            lambda_closure_states = set()
            for state in moved_states:
                lambda_closure_states |= lambda_closure(state, transitions_nfa, state)

            if lambda_closure_states not in dfa_states:
                dfa_states.append(lambda_closure_states)
                if bool(lambda_closure_states.intersection(A_nfa)):
                    dfa_accepting_states.append(lambda_closure_states)
                queue.put(lambda_closure_states)

            dfa_transitions.append((current_states, symbol, lambda_closure_states))

    return {'states' : dfa_states, 'Sigma' : Sigma, 'q0' : initial_closure, \
            'Accepting states' : dfa_accepting_states, 'transitions' : dfa_transitions}

def DFA_simulation(states, Sigma, dfa_q0, dfa_accepting_states, transitions, test_string):
    current_state = dfa_q0
    for symbol in test_string:
        transition_exist = False
        for transition in transitions:
            qi, transition_symbol, qj = transition
            if qi == current_state and transition_symbol == symbol:
                current_state = qj
                transition_exist = True
                break
        if not transition_exist:
            return False
    return current_state in dfa_accepting_states

DFA = NFA_to_DFA_conversion(states_nfa, Sigma, q0_nfa, A_nfa, transitions_nfa)
for test in Test_Cases:
    status = DFA_simulation(DFA['states'], DFA['Sigma'], DFA['q0'],\
                           DFA['Accepting states'], DFA['transitions'], test)
    print("YES") if status else print("NO")