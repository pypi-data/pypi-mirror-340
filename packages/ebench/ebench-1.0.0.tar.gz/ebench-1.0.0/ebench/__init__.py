# Copyright 2025 The KaiJIN Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================


# if __name__ == '__main__':
#   parser = argparse.ArgumentParser(description='Benchmark Executor')
#   parser.add_argument('-t', '--task', type=str, default=None, required=True, help='task name.')
#   parser.add_argument('-f', '--folder', type=str, default=None, help='image/video folder path.')
#   parser.add_argument('-n', '--name', nargs='+', type=str, default=None, help='dataset names.')
#   parser.add_argument('-d', '--dst', type=str, default=None, help='output dataset name.')
#   parser.add_argument('-s', '--split', type=str, default=None, help='dataset split method.')
#   parser.add_argument('-e', '--evaluator', type=str, nargs='+', default=None, help='evaluator names.')
#   parser.add_argument('-m', '--model', type=str, default=None, help='model name.')
#   args = parser.parse_args()

#   if args.task.starswith('dataset'):

#     import dataset

#     if args.task == 'dataset.prepare':
#       dataset.prepare(root=args.folder, name=args.name)

#     elif args.task == 'dataset.view':
#       dataset.view(name=args.name)

#     elif args.task == 'dataset.tag':
#       dataset.tag(name=args.name, dst=args.dst, evaluators=args.evaluator)

#   elif args.task == 'compare':
#     import compare
#     compare.compare(names=args.name, evaluators=args.evaluator, split=args.split)

#   elif args.task == 'enhance':
#     import model
#     model.predict(model=args.model, name=args.name, dst=args.dst)

#   elif args.task == 'summary':
#     import summary
#     summary.summary(names=args.name)
