---
Title: What is the Guid in .NET?
slug: donet-guid
Tags: .NET
status: draft
excerpt: This is the summary for a post
---

After having done some online reseach I found that a Guid in .NET is probably a UUID version 4. Let's put that to the test.

I found several online resources that say something about .NET's `System.Guid`. Some of them are spot on, but not complete, but most of them say is't Microsofts implementation of a [UUID](https://web.archive.org/web/20060615195933/http://www.webdav.org/specs/draft-leach-uuids-guids-01.txt). These explanations are also right, but not complete. So here is my take on `System.Guid`. First to get the obvious out of the way. _GUID_ is an acronym for _Globally Unique Identifier_ and _UUID_ for _Universally Unique Identifier_. Nice to know but not very helpful. As you already know it is used by Microsoft in the .NET ecosystem. A lot of people seem to think it is exclusively used by Microsoft, but that's not true. It is also used by Oracle which has [`SYS_GUID`](https://docs.oracle.com/cd/B12037_01/server.101/b10759/functions153.htm) and C++ has a [`CoCreateGuide()`](https://docs.microsoft.com/en-us/windows/desktop/api/combaseapi/nf-combaseapi-cocreateguid) function. I'm sure there are more implementation that use Guid, but I haven't looked for them since that's not the point of this post.

I found a post on MSDN[^1] with a discussion whether `System.Guid` produces a UUID version 4, but even that thread couldn't rule everything out. So I wrote a simple script to put it to the test. The proposed standard on IETF[^2] states _the UUID version is in the most significant 4 bits of the time stamp (bits 4 through 7 of the time_hi_and_version field)_. This means it should be the fifteenth character in the UUID. So let's print out a couple of Guids to the console and have a look:

[gist:id=7206ed44b09a8cc0c2a49f32ee8c3b40,file=a-list-of-guids-version-4]

## Let's put it to the test

The example above looks like `System.Guid` is indeed a version 4 UUID. But then again, printing out 10 items doesn't really rule out that other values might occur, so lets print a couple more. I created a console application with the following script, which will generate 10 million Guids and verify whether each Guid is indeed a UUID version 4. Each time a Guid is found that isn't version 4 the `Errors found` value will increase.

[gist:id=7206ed44b09a8cc0c2a49f32ee8c3b40,file=Program.cs]

This shows the output below. I ran this test a couple of times and the results are the same every time I ran it. The conclusion I can draw from is this that it is __very__ likely that `System.Guid` is a UUID version 4. 

[gist:id=7206ed44b09a8cc0c2a49f32ee8c3b40,file=test-results-10-million-guids]

## UUID

Now that we know `System.Guid` is a UUID version 4, let's see what that means. After looking at the specification[^3] I draw this conclusion:

- All UUID are fixed-size 128-bits
- A UUID uses the IEEE 802 address (MAC Address) which is usually available on all network attached systems
- The table below shows how the format of a UUID. (An octed is equivalent to a byte)

| Field                     | Data Type               | Octet # | Note                                                                 |
| ------------------------- | ----------------------- | ------- | -------------------------------------------------------------------- |
| time_low                  | unsigned 32 bit integer | 0-3     | The low field of the timestamp.                                      |
| time_mid                  | unsigned 16 bit integer | 4-5     | The middle field of the timestamp.                                   |
| time_hi_and_version       | unsigned 16 bit integer | 6-7     | The high field of the timestamp multiplexed with the version number. |
| clock_seq_hi_and_reserved | unsigned 8 bit integer  | 8       | The high field of theclock sequence multiplexed with the variant.    |
| clock_seq_low             | unsigned 8 bit integer  | 9       | The low field of the clock sequence.                                 |
| node                      | unsigned 48 bit integer | 10-15   | The spatially unique node identifier.                                |

So how does this look? Here is an example with a breakdown. As we have already seen before, the time stamp is in the most significant 4 bits of time_hi_and_version.

[gist:id=7206ed44b09a8cc0c2a49f32ee8c3b40,file=uuid-breakdown]

### UUID Version 4

So far everything is the same for each UUID version. Let's look at some traits that are specific to a UUID Version 4.

#### Algorithm

The version 4 UUID is meant for generating UUIDs from truly-random or pseudo-random numbers.

The algorithm is as follows [^4]: 

- Set the two most significant bits (bits 6 and 7) of the clock_seq_hi_and_reserved to zero and one, respectively.
- Set the four most significant bits (bits 12 through 15) of the time_hi_and_version field to the 4-bit version as described above.
- Set all the other bits to randomly (or pseudo-randomly) chosen values.

I haven't been able to find the exact implementation of `System.Guid.NewGuid()`, so if you can help me out here that would be great.

#### Number of unique values

Give the information above I made the following calculation:

A UUID is 128 bits, but UUID version 4 (a GUID) uses 4 bits for the version and two more bits in clock_seq_hi_and_reserved. Leaving us 122 bits left to work with.
So this gives us `2^122` or about `5.32 * 10^37` possibilities. This is a huge number, so let's try to put this into some perspecive.

- It's about `7 * 10^26` possibilities for each person on the planet.
- If every person on the planet would generate `2.23 * 10^17` or `223.901.956.150.523.000` GUIDs every second for the next 100 years, then we would almost reach the maximum number of possibilities.
- That's almost an Quintillion possibilities for each second for every person on the planet in the next 100 years.

Let's just be honest, that is a huge number. But still, since the values are randomly generated, it's not possible to guarantee a value.

There you have it. My definition of a Guid you can use in C#.

If you have any other insights on this topic or you found a mistake, please let me know in the comments.

#### Sources

[^1]: [Thread on MSDN on System.Guid](https://social.msdn.microsoft.com/Forums/en-US/4956142a-0a5d-4f1e-b102-93a3eea1b5d5/does-guidnewguid-produce-uuid-version-4-according-to-rfc4122?forum=netfxbcl)
[^2]: [IETF proposed UUID Standard](https://tools.ietf.org/html/rfc4122#section-4.1.3)
[^3]: [UUIDs and GUIDs](https://web.archive.org/web/20060615195933/http://www.webdav.org/specs/draft-leach-uuids-guids-01.txt)
[^4]: [UUID Version 4 algorithm](https://tools.ietf.org/html/rfc4122#section-4.4)
