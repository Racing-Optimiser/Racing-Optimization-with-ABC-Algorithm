import CarFailure

tw = 20 #s time spend on switching wheels
tf = 2 #[liter/s] time spend on refueling 1 liter
tr = f(tr) # time spent on repairs\



failure_list = CarFailure.load_from_file('failure_list.json')

def pit_stop_time(tw,tf,tr,am_of_fuel):
    if tr < 15:
        return tw + tf * am_of_fuel + tr
    