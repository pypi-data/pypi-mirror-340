import matplotlib.pyplot as plt
import numpy as np

def hourly_events(Discharge, Dates):

    a = open(Discharge, 'r')
    a1 = open(Dates, 'r')
    b = []
    b1 = []
    for lines in a:
        #c = we strip the lines with c, making every line an item
        c = lines.strip()
        d = lines.split()
        b.append(d)
    a.close()

    for lines in a1:
        #c = we strip the lines with c, making every line an item
        c = lines.strip()
        d = lines.split()
        b1.append(d)
    a1.close()


    #     print(b)
    #     print(len(b))
    #     print('\n')
    #     print(b1)
    #     print(len(b1))
    #     print('\n')
    #     
    Discharge = []
    Dates = []
    for elements in b:
        if len(elements) < 1:
            elements = '0'
            Discharge.append(float(elements))
    #             print(elements)
        else:
    #             print(elements)
            Discharge.append(float(elements[0]))

    for elements in b1:
        Dates.append((elements))
        
    print('\n')        
#     print(f'''Discharge:
# {Discharge}''')
#     print(len(Discharge))
#     print('\n')
#     print(f'''Dates:
# {Dates}''')
#     print(len(Dates))
#     print('\n')

    percentage_discharge_change = ['event']
    for elements in range(1, len(Discharge)):
        y = Discharge[elements]
        change = y - Discharge[elements - 1]
        if Discharge[elements - 1 ] == 0:
            percentage_discharge_change.append('no flow')
        else:
            percent_change = (change/Discharge[elements - 1]) * 100
            percentage_discharge_change.append(percent_change)
        
    # print(f'''Discharge Percentage change
    # {percentage_discharge_change}''')
#     print(len(percentage_discharge_change))
#     print('\n')
    
#     this part of the code prints out the changes in the flow and the serial number
    for elements in range(0, len(percentage_discharge_change)):
        c = f'{elements + 1} - {percentage_discharge_change[elements]}'
#         print(c)
    high_compound_flow = []
    low_compound_flow = []
    combine_compound_flow = []
    events = []
    event_dates = []
    baseflow = []
    baseflow_dates = []
    event_endpoint = 0
    event_bunch = []
    catch_no = 0
    packer = 0
    caught_events = {}
    event_occuring = False
    switch = False
    event_point = float(input('What is the value of the event start point: '))
    if Discharge[0] > event_point:       
        event_occuring = True
        ## this part supplies the whole data for the analysis
    event_ends = 0
    base_compound = 0
    high_compound = 0
    for elements in range(0, len(Discharge)):
#         event_ends = 0
#         base_compound = 0
#         high_compound = 0
        last_slope = -1
        if event_occuring and elements >= len(events):
            truncated_list = Discharge[elements:]
            section_dates = Dates[elements:]
            changing_flow = percentage_discharge_change[elements:]
            ## this part sections the whole data at event point and works on it until the event ends
            for elements1 in range(0, len(truncated_list)):
#                 the part logs the event
                if event_occuring:
                    if truncated_list[elements1] > event_point:
                        event_ends = 0
                        if elements1 > 0:
                            if changing_flow[elements1] == 'no flow':
                                changing_flow[elements1] = 0.0000000001
                            if changing_flow[elements1] < 0:
                                events.append(truncated_list[elements1])
                                event_dates.append(section_dates[elements1])
                                last_slope = changing_flow[elements1]
                                baseflow.append('')
                            else:
                                if last_slope < 0:
                                    high_compound += 1
                                    events.append(truncated_list[elements1])
                                    event_dates.append(section_dates[elements1])
                                    last_slope = changing_flow[elements1]
                                    baseflow.append('')
                                else:
                                    events.append(truncated_list[elements1])
                                    event_dates.append(section_dates[elements1])
                                    last_slope = changing_flow[elements1]
                                    baseflow.append('')
                        else:
                            event_ends = 0
                            events.append(truncated_list[elements1])
                            event_dates.append(section_dates[elements1])
                            baseflow.append('')
#                         the part checks if the event is ended and if base flow as begun
                    else:                        
                        event_ends += 1
                        if event_ends < 2:
                            events.append(truncated_list[elements1])
                            event_dates.append(section_dates[elements1])
                            drop_1 = truncated_list[elements1]
                            baseflow.append('')
                        #this part checks if a compount event begins after reaching baseflow treshold
                        else:
                            if truncated_list[elements1] <= drop_1:
                                baseflow.append(truncated_list[elements1])
                                baseflow_dates.append(section_dates[elements1])
                                event_occuring = False
                                switch = True
                                event_endpoint = elements1
                                events.append('')
                            else:
#                             This part check if it is a slight bump, is significant to creat compound event
                                if truncated_list[elements1] <= event_point:
                                    baseflow.append(truncated_list[elements1])
                                    baseflow_dates.append(section_dates[elements1])
                                    events.append('')
                                    event_occuring = False
                                    switch = True
                                    event_endpoint = elements1
                                else:
                                    base_compound += 1
                                    events.append(truncated_list[elements1])
                                    event_dates.append(section_dates[elements1])
                                    baseflow.append('')
        else:
            if len(events) > 0 and len(events) >= packer and switch == True:
                catch_no += 1
                event_bunch.append(events)
                packer = len(events)
                caught_events[f'{catch_no} event '] = f'{event_dates[0]} - {event_dates[-1]}'
                switch = False
                if high_compound > 1:
                    if base_compound > 1:
                        combine_compound_flow.append(f'{event_dates[0]} - {event_dates[-1]}')
                    else:
                        high_compound_flow.append(f'{event_dates[0]} - {event_dates[-1]}')
                elif base_compound > 1:
                    low_compound_flow.append(f'{event_dates[0]} - {event_dates[-1]}')
                    
            if elements >= len(events):
                if Discharge[elements] >= event_point:
                    event_ends = 0
                    event_dates = []
                    event_occuring = True
                    if event_occuring and elements >= len(events):
                        truncated_list = Discharge[elements:]
                        section_dates = Dates[elements:]
                        changing_flow = percentage_discharge_change[elements:]
                        ## this part sections the whole data at event point and works on it until the event ends
                        for elements1 in range(0, len(truncated_list)):
            #                 the part logs the event
                            if event_occuring:
                                if truncated_list[elements1] > event_point:
                                    event_ends = 0
                                    if elements1 > 0:
                                        if changing_flow[elements1] == 'no flow':
                                            changing_flow[elements1] = 0.0000000001
                                        if changing_flow[elements1] < 0:
                                            events.append(truncated_list[elements1])
                                            event_dates.append(section_dates[elements1])
                                            last_slope = changing_flow[elements1]
                                            baseflow.append('')
                                        else:
                                            if last_slope < 0:
                                                high_compound += 1
                                                events.append(truncated_list[elements1])
                                                event_dates.append(section_dates[elements1])
                                                last_slope = changing_flow[elements1]
                                                baseflow.append('')
                                            else:
                                                events.append(truncated_list[elements1])
                                                event_dates.append(section_dates[elements1])
                                                last_slope = changing_flow[elements1]
                                                baseflow.append('')
                                    else:
                                        event_ends = 0
                                        events.append(truncated_list[elements1])
                                        event_dates.append(section_dates[elements1])
                                        baseflow.append('')
            #                         the part chech if the event is ended and if base flow as begun
                                else:                        
                                    event_ends += 1
                                    if event_ends < 2:
                                        events.append(truncated_list[elements1])
                                        event_dates.append(section_dates[elements1])
                                        drop_1 = truncated_list[elements1]
                                        baseflow.append('')
                                    #this part checks if a compount event begins after reaching baseflow treshold
                                    else:
                                        if truncated_list[elements1] <= drop_1:
                                            baseflow.append(truncated_list[elements1])
                                            baseflow_dates.append(section_dates[elements1])
                                            event_occuring = False
                                            switch = True
                                            event_endpoint = elements1
                                            events.append('')
                                        else:
            #                             This part check if it is a slight bump, is significant to creat compound event
                                            if truncated_list[elements1] <= event_point:
                                                baseflow.append(truncated_list[elements1])
                                                baseflow_dates.append(section_dates[elements1])
                                                events.append('')
                                                event_occuring = False
                                                switch = True
                                                event_endpoint = elements1
                                            else:
                                                base_compound += 1
                                                events.append(truncated_list[elements1])
                                                event_dates.append(section_dates[elements1])
                                                baseflow.append('')
                    else:
                        if len(events) > 0 and len(events) >= packer and switch == True:
                            catch_no += 1
                            event_bunch.append(events)
                            packer = len(events)
                            caught_events[f'{catch_no} event '] = f'{event_dates[0]} - {event_dates[-1]}'
                            switch = False
                            if high_compound > 1:
                                if base_compound > 1:
                                    combine_compound_flow.append(f'{event_dates[0]} - {event_dates[-1]}')
                                else:
                                    high_compound_flow.append(f'{event_dates[0]} - {event_dates[-1]}')
                            elif base_compound > 1:
                                low_compound_flow.append(f'{event_dates[0]} - {event_dates[-1]}')
         
                else:
                    baseflow.append(Discharge[elements])
                    baseflow_dates.append(Dates[elements])
                    events.append('')                        
    
    # print(event_endpoint)            
    # print(f'''events -
    # {events}''')
    # print(len(events))
    # print('\n')
    
#     print(f'''event_dates -
#     {event_dates}''')
#     print(len(event_dates))
#     print('\n')
    
    # print(f'''Baseflow -
    # {baseflow}''')
    # print(len(baseflow))
    # print('\n')
    # print(f'''Baseflow Dates -
    # {baseflow_dates}''')
    # print(len(baseflow_dates))
    # print('\n')
    # print(f'''Event Bunch -
    # {event_bunch}''')
    # print(len(event_bunch))
    # print('\n')
    print(f'''Caught_event -
    {caught_events}''')
    print(len(caught_events))
    print('\n')
    print(f'Number of events - {len(caught_events)}')
    print('\n')
    # print(f'''Combine Compound Flows - 
    # {combine_compound_flow}''')
    # print(f'You have {len(combine_compound_flow)} combine compound flows')
    # print('\n')
    # print(f'''High Compound flows - 
    # {high_compound_flow}''')
    # print(f'You have {len(high_compound_flow)} high compound flows')
    # print('\n')
    # print(f'''Low Compound Flows -
    # {low_compound_flow}''')
    # print(f'You have {len(low_compound_flow)} low compound flows')
    # print('\n')

#     batch_no = input('''The data span in hourly is so large we have to print in batches of 8000 lines
# 
# what batch would you like to print?
#     for first batch press - 1
#     for second batch press - 2
#     for third batch press - 3
#     etc
#     
#     ''')
#     print('\n')
#     print('Events')
#     try:
#         batch_no = int(batch_no)
#         xx = batch_no - 1
#         Range = 8000
#         start = xx * Range
#         for elements in range(0, len(events)):
#             if elements >= start and elements <= start + Range - 1:
#                 print(events[elements])
#         print('End')
#         
#     except:
#         print('ERROR')
#         print('Batch Number must be integer')
#         exit()
    
    valid_drop = event_point * 1.25
    for elements in range (0, len(events)):
        if type(events[elements]) == float:
            if elements > 0 and events[elements] > valid_drop:
                events[elements - 1] = Discharge[elements - 1]
    
    file_name = "hourly_flow_event_data.txt"
        # Write to file (small predicted data)
    with open(file_name, "w") as file:
        for number in events:
            file.write(f"{number}\n")
    print(f"Numbers successfully written to {file_name}")

    if len(Discharge) < 5000:
        y2 = events
        y1 = Discharge
        
        x = []
        for elements in range(0, len(y1)):
            x.append(elements)

        # Convert empty strings to np.nan and the rest to float for y2
        y2_clean = [float(val) if val != '' else np.nan for val in y2]

        # Create stacked subplots with shared x-axis
        fig, axs = plt.subplots(2, 1, figsize=(6, 6), sharex=True)

        # First plot (y1)
        axs[0].plot(x, y1, marker='', color='green')
        axs[0].set_title('Plot of Discharge Data')
        axs[0].set_ylabel('Drainage (cm3/day)')
        axs[0].grid(False)

        # Second plot (y2 with missing)
        axs[1].plot(x, y2_clean, marker='', linestyle='-', color='blue')
        axs[1].set_title('Plot of Events')
        axs[1].set_xlabel('Dates')
        axs[1].set_ylabel('Drainage (cm3/day)')
        axs[1].grid(False)
        points = 30
        if len(x) < points:
            points = len(x)
        axs[1].xaxis.set_major_locator(plt.MaxNLocator(nbins=points))
        fig.autofmt_xdate(rotation=45)

        # Optional: Set same y-axis limits (uncomment if needed)
        y_min = min(min(y1, default=np.nan), min(y2_clean, default=np.nan))
        y_max = max(max(y1, default=np.nan), max(y2_clean, default=np.nan))
        if not np.isnan(y_min) and not np.isnan(y_max):
            axs[0].set_ylim(y_min, y_max)
            axs[1].set_ylim(y_min, y_max)

        # Adjust layout and show
        plt.tight_layout()
        plt.show()

Discharge = 'hourly_event_data.txt'
Dates = 'Hourly_Dates.txt'

hourly_events(Discharge, Dates)
