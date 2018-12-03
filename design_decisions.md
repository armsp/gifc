## script vs a full fledged process
Examples of full fledged process-

- fish
- docker toolbox

gifc is a sparingly used utility. You may need it only a few times a day or a month (relative to how often you type commands in fish or docker toolbox for example). So it doesn't make sense to have it as a process that you need to exit explicitly.
The frequency of commands you type would be much much lower than say when you use fish or docker-toolbox.  
So we can afford to load the two variables from file system everytime instead of reading it once per process.  

## script vs entry_point

## pure python vs mixture of python and shell (and others)
Supporting other platforms would be a pain, the more languages we add. Keep it smooth and simple so that it works just by a pip install on Windows too.

## requiring dependencies vs using only standard libraries
