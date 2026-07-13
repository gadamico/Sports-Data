def update_db(champ, runner_up, losing_sfs, losing_qfs, which_slam='aus'):
    
    """
    This function updates the mens_tennis database when the latest
    slam results are entered: the champ's and runner-up's names as
    strings, followed by a list of the (two) losing semi-finalists
    and a list of the (four) losing quarter-finalists. (Every name
    should be entered as "Last, First".) The last parameter
    specifies which slam has just happened: Please use one of the
    following codes: {'aus', 'fr', 'wim', 'us'}.
    """
    
    # Make the relevant imports
    import sqlite3
    import pandas as pd
    
    # Connect to the db
    con = sqlite3.connect('/Users/gadamico/Fun/Sports-Data/mens_singles_tennis/data/tennis.db')
    
    # Access the relevant columns
    gen_totals = [2, 3, 4, 5]
        
    slam_col_dict = {'aus': 6, 'fr': 10, 'wim': 14, 'us': 18}
    
    spec_totals = range(slam_col_dict[which_slam], slam_col_dict[which_slam]+4)
    
    # Prepare proper SQL queries
    slam_pref_dict = {'aus': 'Aus_', 'fr': 'Fr_', 'wim': 'Wim_', 'us': 'US_'}
    
    pref = slam_pref_dict[which_slam]
    
    ## CHAMP
    # Access champ's record if existent
    champ_result = pd.read_sql(
        f"""
        SELECT *
        FROM mens_tennis
        WHERE Player = '{champ}'
        """,
        con
    )
    
    
    # If champ exists in db, then update
    if champ_result.shape[0] == 1:
        
        plyr_gen_totals = champ_result.iloc[0, gen_totals]
        
        plyr_spec_totals = champ_result.iloc[0, spec_totals]
        
        con.execute(
            f"""
            UPDATE mens_tennis
            SET QF_Appears = {plyr_gen_totals[0]+1},
            QF_Wins = {plyr_gen_totals[1]+1},
            SF_Wins = {plyr_gen_totals[2]+1},
            F_Wins = {plyr_gen_totals[3]+1},
            {pref}QF_Appears = {plyr_spec_totals[0]+1},
            {pref}QF_Wins = {plyr_spec_totals[1]+1},
            {pref}SF_Wins = {plyr_spec_totals[2]+1},
            {pref}F_Wins = {plyr_spec_totals[3]+1},

            WHERE Player = '{champ}'
            """
            )
    
    # Otherwise, add him:
    else:
        
        # Get new row number
        new_no = pd.read_sql(
        """
        SELECT *
        FROM mens_tennis
        ORDER BY rowid DESC
        LIMIT 1
        """
        ,
        con)['index'][0] + 1
        
        if which_slam == 'aus':
            
            con.execute(
                f"""
                INSERT INTO mens_tennis
                VALUES ({new_no}, '{champ}', 1, 1, 1, 1, 1, 1, 1, 1, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
                """
                )
        
        elif which_slam == 'fr':
            
            con.execute(
                f"""
                INSERT INTO mens_tennis
                VALUES ({new_no}, '{champ}', 1, 1, 1, 1, 0, 0, 0, 0, 1, 1,
                1, 1, 0, 0, 0, 0, 0, 0, 0, 0)
                """
                )
        
        elif which_slam == 'wim':
            
            con.execute(
                f"""
                INSERT INTO mens_tennis
                VALUES ({new_no}, '{champ}', 1, 1, 1, 1, 0, 0, 0, 0, 0, 0,
                0, 0, 1, 1, 1, 1, 0, 0, 0, 0)
                """
                )
        
        else:
            
            con.execute(
                f"""
                INSERT INTO mens_tennis
                VALUES ({new_no}, '{champ}', 1, 1, 1, 1, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 1, 1, 1, 1)
                """
                )
        
    ## RUNNER-UP
    # Access runner-up's record if existent
    runner_up_result = pd.read_sql(
        f"""
        SELECT *
        FROM mens_tennis
        WHERE Player = '{runner_up}'
        """
        ,
        con
    )

    # If runner-up exists in db, then update
    if runner_up_result.shape[0] == 1:

        plyr_gen_totals = runner_up_result.iloc[0, gen_totals]

        plyr_spec_totals = runner_up_result.iloc[0, spec_totals]

        con.execute(
            f"""
            UPDATE mens_tennis
            SET QF_Appears = {plyr_gen_totals[0]+1},
            QF_Wins = {plyr_gen_totals[1]+1},
            SF_Wins = {plyr_gen_totals[2]+1},
            {pref}QF_Appears = {plyr_spec_totals[0]+1},
            {pref}QF_Wins = {plyr_spec_totals[1]+1},
            {pref}SF_Wins = {plyr_spec_total[2]+1}

            WHERE Player = '{runner_up}'
            """
            )

    # Otherwise, add him:
    else:

        # Get new row number
        new_no = pd.read_sql(
        """
        SELECT *
        FROM mens_tennis
        ORDER BY rowid DESC
        LIMIT 1
        """
        ,
        con)['index'][0] + 1

        if which_slam == 'aus':

            con.execute(
                f"""
                INSERT INTO mens_tennis
                VALUES ({new_no}, '{runner_up}', 1, 1, 1, 0, 1, 1, 1, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
                """
                )

        elif which_slam == 'fr':

            con.execute(
                f"""
                INSERT INTO mens_tennis
                VALUES ({new_no}, '{runner_up}', 1, 1, 1, 0, 0, 0, 0, 0, 1, 1,
                1, 0, 0, 0, 0, 0, 0, 0, 0, 0)
                """
                )

        elif which_slam == 'wim':

            con.execute(
                f"""
                INSERT INTO mens_tennis
                VALUES ({new_no}, '{runner_up}', 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 1, 1, 1, 0, 0, 0, 0, 0)
                """
                )

        else:

            con.execute(
                f"""
                INSERT INTO mens_tennis
                VALUES ({new_no}, '{runner_up}', 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 1, 1, 1, 0)
                """
                )
            
    ## LOSING SFs
    for player in losing_sfs:

        # Access record if existent
        sf_result = pd.read_sql(
        f"""
        SELECT *
        FROM mens_tennis
        WHERE Player = '{player}'
        """
        ,
        con
        )

        # If player exists in db, then update
        if sf_result.shape[0] == 1:

            plyr_gen_totals = sf_result.iloc[0, gen_totals]

            plyr_spec_totals = sf_result.iloc[0, spec_totals]

            con.execute(
                f"""
                UPDATE mens_tennis
                SET QF_Appears = {plyr_gen_totals[0]+1},
                QF_Wins = {plyr_gen_totals[1]+1},
                {pref}QF_Appears = {plyr_spec_totals[0]+1},
                {pref}QF_Wins = {plyr_spec_totals[1]+1}

                WHERE Player = '{player}'
                """
                )

        # Otherwise, add him:
        else:

            # Get new row number
            new_no = pd.read_sql(
            """
            SELECT *
            FROM mens_tennis
            ORDER BY rowid DESC
            LIMIT 1
            """
            ,
            con)['index'][0] + 1

            if which_slam == 'aus':

                con.execute(
                    f"""
                    INSERT INTO mens_tennis
                    VALUES ({new_no}, '{player}', 1, 1, 0, 0, 1, 1, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
                    """
                    )

            elif which_slam == 'fr':

                con.execute(
                    f"""
                    INSERT INTO mens_tennis
                    VALUES ({new_no}, '{player}', 1, 1, 0, 0, 0, 0, 0, 0, 1, 1,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
                    """
                    )

            elif which_slam == 'wim':

                con.execute(
                    f"""
                    INSERT INTO mens_tennis
                    VALUES ({new_no}, '{player}', 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 1, 1, 0, 0, 0, 0, 0, 0)
                    """
                    )

            else:

                con.execute(
                    f"""
                    INSERT INTO mens_tennis
                    VALUES ({new_no}, '{player}', 1, 1, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 1, 1, 0, 0)
                    """
                    )
    ## LOSING QFs
    for player in losing_qfs:

        # Access record if existent
        qf_result = pd.read_sql(
        f"""
        SELECT *
        FROM mens_tennis
        WHERE Player = '{player}'
        """
        ,
        con
        )

        # If player exists in db, then update
        if qf_result.shape[0] == 1:

            plyr_gen_totals = qf_result.iloc[0, gen_totals]

            plyr_spec_totals = qf_result.iloc[0, spec_totals]

            con.execute(
                f"""
                UPDATE mens_tennis
                SET QF_Appears = {plyr_gen_totals[0]+1},
                {pref}QF_Appears = {plyr_spec_totals[0]+1}

                WHERE Player = '{player}'
                """
                )

        # Otherwise, add him:
        else:

            # Get new row number
            new_no = pd.read_sql(
            """
            SELECT *
            FROM mens_tennis
            ORDER BY rowid DESC
            LIMIT 1
            """
            ,
            con)['index'][0] + 1

            if which_slam == 'aus':

                con.execute(
                    f"""
                    INSERT INTO mens_tennis
                    VALUES ({new_no}, '{player}', 1, 0, 0, 0, 1, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
                    """
                    )

            elif which_slam == 'fr':

                con.execute(
                    f"""
                    INSERT INTO mens_tennis
                    VALUES ({new_no}, '{player}', 1, 0, 0, 0, 0, 0, 0, 0, 1, 0,
                    0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
                    """
                    )

            elif which_slam == 'wim':

                con.execute(
                    f"""
                    INSERT INTO mens_tennis
                    VALUES ({new_no}, '{player}', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 1, 0, 0, 0, 0, 0, 0, 0)
                    """
                    )

            else:

                con.execute(
                    f"""
                    INSERT INTO mens_tennis
                    VALUES ({new_no}, '{player}', 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                    0, 0, 0, 0, 0, 0, 1, 0, 0, 0)
                    """
                    )