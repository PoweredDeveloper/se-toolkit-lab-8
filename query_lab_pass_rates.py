#!/usr/bin/env python3
"""Query all labs and their completion rates to find the lowest pass rate."""

import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import select, func, case, cast, Numeric
from sqlmodel import SQLModel, col


# Database connection string
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "db-lab-8"
DB_USER = "postgres"
DB_PASSWORD = "postgres"

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


async def get_lab_pass_rates():
    """Query all labs and their completion rates."""
    engine = create_async_engine(DATABASE_URL, echo=False)
    
    async with AsyncSession(engine) as session:
        # First, get all labs
        from sqlmodel import text
        
        # Get all lab items
        result = await session.exec(
            text("SELECT id, title FROM item WHERE type = 'lab' ORDER BY title")
        )
        labs = result.all()
        
        if not labs:
            print("No labs found in the database.")
            print("The database might be empty or not populated yet.")
            return
        
        print(f"Found {len(labs)} labs:\n")
        print(f"{'Lab ID':<10} {'Title':<40} {'Completion Rate':<20} {'Passed':<10} {'Total':<10}")
        print("-" * 95)
        
        results = []
        
        for lab_id, lab_title in labs:
            # Get child task IDs for this lab
            task_result = await session.exec(
                text(f"SELECT id FROM item WHERE parent_id = {lab_id}")
            )
            task_ids = [row[0] for row in task_result.all()]
            
            if not task_ids:
                # No tasks, skip or show 0%
                results.append((lab_id, lab_title, 0.0, 0, 0))
                continue
            
            # Count distinct learners with any interaction in this lab
            all_items = [lab_id] + task_ids
            items_str = ",".join(str(i) for i in all_items)
            
            # Total learners
            total_result = await session.exec(
                text(f"""
                    SELECT COUNT(DISTINCT learner_id) 
                    FROM interacts 
                    WHERE item_id IN ({items_str})
                """)
            )
            total_learners = total_result.scalar() or 0
            
            # Passed learners (score >= 60)
            passed_result = await session.exec(
                text(f"""
                    SELECT COUNT(DISTINCT learner_id) 
                    FROM interacts 
                    WHERE item_id IN ({items_str}) AND score >= 60
                """)
            )
            passed_learners = passed_result.scalar() or 0
            
            # Calculate completion rate
            if total_learners > 0:
                completion_rate = (passed_learners / total_learners) * 100
            else:
                completion_rate = 0.0
            
            results.append((lab_id, lab_title, completion_rate, passed_learners, total_learners))
        
        # Print results
        for lab_id, lab_title, rate, passed, total in results:
            print(f"{lab_id:<10} {lab_title:<40} {rate:>6.1f}%{'':<12} {passed:<10} {total:<10}")
        
        # Find the lab with the lowest pass rate
        if results:
            # Filter out labs with 0 total learners (no data)
            valid_results = [(lab_id, title, rate, passed, total) 
                           for lab_id, title, rate, passed, total in results 
                           if total > 0]
            
            if valid_results:
                lowest_lab = min(valid_results, key=lambda x: x[2])
                print("\n" + "=" * 95)
                print(f"\n📊 Lab with LOWEST pass rate:")
                print(f"   Lab ID: {lowest_lab[0]}")
                print(f"   Title: {lowest_lab[1]}")
                print(f"   Completion Rate: {lowest_lab[2]:.1f}%")
                print(f"   Passed: {lowest_lab[3]} / Total: {lowest_lab[4]}")
            else:
                print("\nNo labs with interaction data found.")
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(get_lab_pass_rates())
