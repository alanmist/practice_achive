from collections import deque
import random
import time


def customer_simulation(simulation_time=10,probabily_of_arival=0.35,seed=None):
    if seed is not None:
        random.seed(seed)
    
    
    customer=deque()
    next_id= 1
    wait_times=[]
    max_customer=0
    serving=False

   
    
    print("Stating...... (Simulation bank queue)")
    for num in range(simulation_time):
        if random.random()< probabily_of_arival:
                
            customer.append((next_id,num))
                
            print(f"[Time={num:02d}] arives -> customer{next_id}-> (Queue={len(customer)})")
            next_id+=1
        
        else:
                
            print(f'[Time={num:02d} no one arives (queue={len(customer)})')
        
        if not serving and customer:
            serving=True

            customer_id, arive_time=customer.popleft()
            wait=num-arive_time
            wait_times.append(wait)
            print(f"severd  customer {customer_id} wait={wait} quw={len(customer)}")
        
        else:
            if serving:
                serving=False
                print(f'[Time={num:02d}]finished serving customer, queue={len(customer)}')
        max_customer=max(max_customer,len(customer))


    served=len(wait_times)
    avg_wait=sum(wait_times)/served if served else 0.0
    print('\n summery')
    print(f"ticks: {simulation_time}")
    print(f'served: {served}')
    print(f"avg wait: {avg_wait:.2f}")
    print(f'max que :{max_customer}')
        

customer_simulation(50,0.4)