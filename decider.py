# hello_decider.py
import boto.swf.layer2 as swf
import time,logging
logging.basicConfig(filename='/var/log/app/app.log',level=logging.INFO)

DOMAIN = 'demo'
ACTIVITY = 'HelloWorld'
VERSION = '1.0'
TASKLIST = 'default'

class HelloDecider(swf.Decider):

    domain = DOMAIN
    task_list = TASKLIST
    version = VERSION

    def run(self):
        while True:
            history = self.poll()
            if 'events' in history:
                # Find workflow events not related to decision scheduling.
                workflow_events = [e for e in history['events']
                    if not e['eventType'].startswith('Decision')]
                last_event = workflow_events[-1]

                decisions = swf.Layer1Decisions()
                if last_event['eventType'] == 'WorkflowExecutionStarted':
                    decisions.schedule_activity_task('saying_hi', ACTIVITY, VERSION, task_list=TASKLIST)
                    logging.info(str(time.time()))
                elif last_event['eventType'] == 'ActivityTaskCompleted':
                    decisions.complete_workflow_execution()
                self.complete(decisions=decisions)
            if history is False:
                history = "No decisions to make"

if __name__ == '__main__':
    HelloDecider().run()