# debugging interface

We accessed the embedded device's asynchronous serial debugging interface while it was operational and captured some messages that were being transmitted over it. Can you decode them? <br>
https://app.hackthebox.com/challenges/debugging-interface

# solution

the challenge downloaded after unzipping has the .sal ending, which is a file created with the salae logic tool. <br>

- it can be examined too with the salae logic 2 tool.
- https://discuss.saleae.com/t/utilities-for-sal-files/725
- https://www.saleae.com/downloads/

as the provided file is asynchronous serial debugging communication the "async serial" analyzer is used. <br>
to calculate the baud rate used, the time of the first sent bit is taken as divisor with the dividend of 1.000.000 because of microseconds

$$
baudrate = \frac{1000000}{32.02} \newline
$$

this results in a baud rate of 31230. after applying the "async serial" filter with the calculated baud rate the flag can be read out of the data terminal section.
