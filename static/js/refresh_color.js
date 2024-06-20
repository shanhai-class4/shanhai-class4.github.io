			const l1 = 125;
			const l2 = 223;
			const l3 = 215;
			const r1 = 172;
			const r2 = 192;
			const r3 = 232;
			const dl1 = 34;
			const dl2 = 140;
			const dl3 = 131;
			const dr1 = 44;
			const dr2 = 81;
			const dr3 = 158;
			
			const fix1st = 25140; // @06:59
			const fix2st = 73740; // @20:29
			const fixlength = 120; //@2min
			
			function RGB(R, G, B)
			{
				var p = Number(0x1000000 + R * 0x10000 + G * 0x100 + B).toString(16).substring(1);
				return "#" + p;
			}
			function setColor(lRGB, rRGB)
			{
				var tmp = document.body;
				var dat = "linear-gradient(99deg, " + lRGB + ", " + rRGB + ")";
				tmp.style.backgroundImage = dat;
			}
			function getTimeStamp()
			{
				var d =  new Date();
				var h = d.getHours();
				var m = d.getMinutes();
				var s = d.getSeconds();
				return h * 3600 + m * 60 + s;
			}
			function getLRGB(timestamp)
			{
				var tc;
				if (timestamp > fix1st + fixlength && timestamp <= fix2st)
				{
					tc = 0;
				}
				else if (timestamp <= fix1st || timestamp > fix2st + fixlength)
				{
					tc = fixlength;
				}
				else if (timestamp > fix1st && timestamp <= fix1st + fixlength)
				{
					tc = fix1st + fixlength + 1 - timestamp;
				}
				else
				{
					tc = timestamp - fix2st;
				}
				tc = fixlength - tc;
				var R = parseInt((l1 - dl1) / fixlength * tc + dl1);
				var G = parseInt((l2 - dl2) / fixlength * tc + dl2);
				var B = parseInt((l3 - dl3) / fixlength * tc + dl3);
				//console.log(tc);
				//console.log(RGB(R, G, B));
				return RGB(R, G, B);
			}
			function getRRGB(timestamp)
			{
				var tc;
				if (timestamp > fix1st + fixlength && timestamp <= fix2st)
				{
					tc = 0;
				}
				else if (timestamp <= fix1st || timestamp > fix2st + fixlength)
				{
					tc = fixlength;
				}
				else if (timestamp > fix1st && timestamp <= fix1st + fixlength)
				{
					tc = fix1st + fixlength + 1 - timestamp;
				}
				else
				{
					tc = timestamp - fix2st;
				}
				tc = fixlength - tc;
				var R = parseInt((r1 - dr1) / fixlength * tc + dr1);
				var G = parseInt((r2 - dr2) / fixlength * tc + dr2);
				var B = parseInt((r3 - dr3) / fixlength * tc + dr3);
				//console.log(tc);
				//console.log(RGB(R, G, B));
				return RGB(R, G, B);
			}
			function refreshColor()
			{
				var st = getTimeStamp();
				var LRGB = getLRGB(st);
				var RRGB = getRRGB(st);
				setColor(LRGB, RRGB);
			}