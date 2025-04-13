import difflib
import ultraprint.common as p
from ..config import Config

def show_content(content, is_new=True):
    """Show content with line numbers and color-coded (green for new, red for deleted)"""
    lines = content.split('\n')
    max_lines = min(Config.MAX_CONTENT_LINES, len(lines))
    
    for i, line in enumerate(lines[:max_lines]):
        if is_new:
            p.green(f"  + {i+1:3d} | {line}")
        else:
            p.red(f"  - {i+1:3d} | {line}")
    
    if len(lines) > max_lines:
        p.dgray(f"  ... {len(lines) - max_lines} more lines not shown")

def show_diff(old_content, new_content):
    """Show git-style diff between old and new content"""
    old_lines = old_content.splitlines()
    new_lines = new_content.splitlines()
    
    differ = difflib.Differ()
    diffs = list(differ.compare(old_lines, new_lines))
    
    # Limit the number of lines shown
    max_lines = Config.MAX_DIFF_LINES
    shown_lines = 0
    context_lines = Config.CONTEXT_LINES  # Number of unchanged lines to show around changes
    
    i = 0
    while i < len(diffs) and shown_lines < max_lines:
        line = diffs[i]
        
        if line.startswith('  '):  # Unchanged line
            # Check if this is near a changed line
            show_context = False
            
            # Look ahead for changes
            for j in range(1, context_lines + 1):
                if i + j < len(diffs) and not diffs[i + j].startswith('  '):
                    show_context = True
                    break
            
            # Look behind for changes
            for j in range(1, context_lines + 1):
                if i - j >= 0 and not diffs[i - j].startswith('  '):
                    show_context = True
                    break
            
            if show_context:
                p.dgray(f"    | {line[2:]}")
                shown_lines += 1
            
        elif line.startswith('- '):  # Removed line
            p.red(f"  - | {line[2:]}")
            shown_lines += 1
            
        elif line.startswith('+ '):  # Added line
            p.green(f"  + | {line[2:]}")
            shown_lines += 1
            
        # Move to next line
        i += 1
    
    if i < len(diffs):
        p.dgray(f"  ... {len(diffs) - i} more changes not shown")
