using System.IO;
using Microsoft.Azure.WebJobs;
using Microsoft.ServiceBus.Messaging;
using Newtonsoft.Json;
using RobotDesk.Core;
using RobotDesk.Core.Data;

namespace RobotDesk.QueueReaderJob
{
    public class Functions
    {
        // This function will get triggered/executed when a new message is written 
        // on an Azure Queue called queue.

        public static void ProcessQueueMessage(
            [ServiceBusTrigger("robotdeskheightchangequeue")] BrokeredMessage message, TextWriter logger) {
            logger.WriteLine("got message!");
            string json = null;
            using (Stream stream = message.GetBody<Stream>())
            using (TextReader reader = new StreamReader(stream)) {
                json = reader.ReadToEnd();
            }
            logger.WriteLine("Received message: " + json);

            HeightLog height = null;
            height = JsonToHeightLog(json);

            var svc = new HeightLogSvc();
            svc.SaveHeightLogEntry(height);
        }


        private static HeightLog JsonToHeightLog(string message) {
            return JsonConvert.DeserializeObject<HeightLog>(message);
        }
    }
}
