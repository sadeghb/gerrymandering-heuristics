def batch_gerrymander(state: list[list[int]], buffer_min_length=1) -> list[list[tuple[int,int]]]:
    """
    This function gerrymanders the hell out of a state.
    The returned districts always incur size_score of 0.
    The returns districts always incur a distance_score of 0, except for n = 5.

    It generally traverses 4 or 5 wide rectangles of almost the same height. Very small n's are treated slightly differently.
    Each rectangle is as wide as the state.
    It traverses the rectangles from top to bottom
    It traverses each rectangle column by column from left to right.
    
    One "winning" and one "losing" district are kept available during the traversal.
    The visited cities are assigned to one of the two districts in a greedy fashion.
    If the candidate in the visited city has adequately high number of votes, that cities goes to the "winning" district.
    Otherwise, it goes to the "losing" district.

    A buffer is used to enhance the performance of the greedy assignment. It serves as a local improvement add-on if you will.
    Its main role is looking ahead a bit to avoid assigning a low vote city to the "winning" district even if it can tolerate it.
    Its other role is to make sure that the two available districts don't wait too long to take a new city.
    This is done by imposing a strict condition that each district gets at least one city from the buffer.
    """    
    n = len(state)
    k = n // 4 # Each rectangle to traverse has a height of k or k + 1
    if n < 12: # Treat very small sizes slightly differently
        k = n // 4 + 1

    q = n // k # Total number of rectangles: 4 (if n is divisible by 4) or 5 (otherwise)
    r = n % k # Number of rectangles of height k + 1

    buffer_max_length = max(buffer_min_length, min(40, n  // 16))

    districts = [] # List of districts
    start_row = 0

    # Traverse q - r rectangles of height k, then r rectangles of height k + 1
    for idx in range(q):
        # Determine the height of the rectangle
        if idx < q - r:
            height = k
        else:
            height = k + 1
        
        # Design traversal path of the rectangle
        rect = [(row, col) for col in range(n) for row in range(start_row, start_row + height)]
        
        rect_districts = 0 # Rectangle's running number of districts
        district_w = []  # Winning district; fingers crossed!
        district_l = [] # Losing district; god forbid!
        w_sum = 0 # Winning district's running sum

        buffer_start = 0
        outer_break = False

        # Traverse rectangle and divide it into *height* districts
        while buffer_start < len(rect):
            
            # Create a buffer to process the cities in groups
            buffer_end = min(buffer_start + buffer_max_length, len(rect))
            buffer = rect[buffer_start: buffer_end]
            buffer.sort(key=lambda city: state[city[0]][city[1]], reverse=True) # Sort the buffer to enhance the greedy choice

            for i, city in enumerate(buffer):
                city_vote = state[city[0]][city[1]]

                # Greedily assign city to *district_w* or *district_l*
                # If the city keeps *district_w* winning, assign it to *district_w*, otherwise asssign it to *district_l*
                
                # By default, the highest vote city goes to *district_w* and lowest vote city goes to *district_l*
                # This is to make sure that distance_score is kept zero
                
                if (i == 0) or (i < len(buffer) - 1 and city_vote + w_sum > 500 * (len(district_w) + 1)): # Case of dequately high vote
                    district_w.append(city)
                    w_sum += city_vote

                    if len(district_w) == n:
                        rect_districts += 1
                        districts.append(district_w)
                        district_w = []
                        w_sum = 0

                else: # Case of inadequate vote
                    district_l.append(city)
                    
                    if len(district_l) == n:
                        rect_districts += 1
                        districts.append(district_l)
                        district_l = []

                if rect_districts == height - 1: # Only one more district is allowed in the rectangle
                    outer_break = True # To then break out of the rectangle
                    last_rect_district = district_w + district_l + buffer[i+1:] # All goes to the last district
                    break # Break out of the buffer

            buffer_start = buffer_end
                
            if outer_break:
                last_rect_district += rect[buffer_end:] # All continues to go to the last district
                districts.append(last_rect_district)
                break # Break out of the rectangle
        
        start_row += height # Prepare for the next rectangle
    
    return districts
